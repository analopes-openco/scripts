# from pyramid.threadlocal import get_current_registry
import transaction
from typing import Dict, List
from app.openco import IOpenCoClient
from app.tvm.infra.db import DBSession
from zope.sqlalchemy import mark_changed
from app.tvm.infra.db.factories import NoteFactory
from app.tvm.infra.db.entities import OUTBOX, INBOX
from app.tvm.domain.models.note import Note, NotePayload
from app.tvm.domain.models import IncomingType, OutgoingType, MessageState
from app.tvm.infra.usecases.openco.granted.enqueue.schemas import (
    OpenCoGrantedPayloadSchema,
)


def get_note(ccb_number: str):
    stmt = (
        INBOX.select()
        .filter(
            INBOX.c.type == IncomingType.NOTE,
            INBOX.c.payload["contract"]["external_identifier"].astext
            == str(ccb_number),
        )
        .order_by(INBOX.c.created.desc())
    )
    row = DBSession.execute(stmt).first()
    return NoteFactory.from_row(row)


def get_outbox_failed_created(execution_uuid: str):
    stmt = OUTBOX.select().filter(
        OUTBOX.c.type == OutgoingType.FAILED,
        OUTBOX.c.execution_uuid == str(execution_uuid),
    )
    row = DBSession.execute(stmt).one_or_none()
    if not row:
        return
    return str(row["created"])


def serialize(note: Note):
    serialized = NotePayload.Schema().dump(note.payload)
    serialized["operation"]["mdr_value"] = (
        serialized.get("operation", {}).get("mdr_value") or 0
    )

    if note.get("funded_at"):
        serialized["operation"]["granted_at"] = note.get("funded_at")

    else:
        failed_created = get_outbox_failed_created(execution_uuid=note.execution_uuid)
        if failed_created:
            serialized["operation"]["granted_at"] = failed_created
        else:
            serialized["operation"]["granted_at"] = note.updated

    serialized["request_uuid"] = str(note.uuid)
    return serialized


def schema(payload: Dict):
    schema = OpenCoGrantedPayloadSchema()
    errors = schema.validate(payload)
    if not errors:
        return payload
    else:
        print(f"SchemaError: {str(errors)}")


def send_granted(payload: Dict):
    client = registry.queryUtility(IOpenCoClient)
    client.granted(payload)


def update_note(uuid: str):
    stmt = (
        INBOX.update()
        .filter(INBOX.c.type == IncomingType.NOTE, INBOX.c.uuid == str(uuid))
        .values(
            {
                INBOX.c.state: MessageState.DONE,
                INBOX.c.reason: "ManualIntervention: success disbursed in scd, but manual granted",
            }
        )
    )
    DBSession.execute(stmt)
    mark_changed(DBSession())


def run(ccbs: List[str]):
    for ccb in ccbs:
        note = get_note(ccb_number=ccb)

        if note and note.workflow in ["geru-note-openscd", "geru-note-qitech"]:
            note_payload = serialize(note=note)
            schema_payload = schema(payload=note_payload)

            try:
                send_granted(payload=schema_payload)
            except Exception as e:
                print(f"CCB_{ccb}: {str(e)}")
            else:
                update_note(uuid=note.uuid)

    transaction.commit()


run(ccbs=[])
