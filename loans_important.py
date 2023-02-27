# import transaction
# import uuid
# import csv
# import json
# from tropicalista.scripts.accounting import display
# from external_services.payment_srv.api import PaymentSRV
# from datetime import date, datetime
# from geru_payments.exceptions import NotFoundOnGateway
# from pyramid_transactional_celery import task_tm
# from tropicalista.models import DBSession
# from tropicalista.models.loan import BookedLoan, Loan, LoanOneNote
# from tropicalista.models.payment import Payment, SettlementPayment
# from tropicalista.models.processing_request import RefundProcessingRequest
# from tropicalista.models.settlement import Settlement
# from tropicalista.utils.money import Decimal
# from tropicalista.models.loan import Loan
# from dozece.utils.interest import InterestCalculator
# from tropicalista.scripts_ran_on_production.utils import cancel_payments
# from geru_intention.manager import PaymentIntentionManager
# from tropicalista.models.payment_method import PaymentMethod
# from tropicalista.models.payment_plan import PaymentPlan, PaymentPlanDueDateChange, PaymentPlanGracePeriod
# from tropicalista.models.instalment import Instalment
# from geru_intention.models import BookedPrePaymentIntention, BookedDuePaymentIntention
# from collections import Counter
# from tropicalista.utils.money import Decimal
# from tropicalista.utils.timezone import today
# from tropicalista.models.note import CCB, Note
# from geru_marketplace.tvm_client import tvm_client
# from geru_marketplace.tvm_client.serializers import (
#     to_tvm_payment_plan_change, to_tvm_settlement, to_tvm_payment)


# LOAN - Consultar payment
# payment = SettlementPayment.get(uuid)
# payment.settlements.all()
# sett = payment.settlements.first()
# sett.loan
# sett.partials.all()
# sett.partials.first()
# sett.partials.first().__dict__
# sett.partials.first().instalment
# sett.partials.first().instalment.balance()

# LOAN - Consultar note
# loan = Loan.query.join(Note).join(CCB).filter(CCB.number == "L13172226").all()
# loan = Loan.query.join(Note, CCB).filter(CCB.number == '<ccb_number>').one()
