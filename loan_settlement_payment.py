from tropicalista.models.payment import SettlementPayment


pay = SettlementPayment.get('2137e2fc-4cd2-44ca-8661-f5c68d249ac5')
payment = SettlementPayment.query.filter(SettlementPayment.uuid == '2137e2fc4cd244ca8661f5c68d249ac5').one()
external_identifier = payment.extradata.get("external_identifier")

payment.settlements.all()
sett = payment.settlements.first()
sett.loan

sett.partials.all()
sett.partials.first()
sett.partials.first().__dict__
sett.partials.first().instalment
sett.partials.first().instalment.balance()
