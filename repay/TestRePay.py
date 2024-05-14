from . import models
def TestRePay(repayOrder):
    repayOrder.state = 3
    repayOrder.save()
    uid = repayOrder.uid
    extenrelation = models.extensionRelation.objects(_id=uid).first()
    if extenrelation:
        extenrelation.tolCashOut = extenrelation.tolCashOut + repayOrder.dinheiro
        extenrelation.save()