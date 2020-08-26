from django.db import models
from apps.ProductInfo.models import ProductInfo
from apps.Supplyer.models import Supplyer


class BuyInfo(models.Model):
    buyId = models.AutoField(primary_key=True, verbose_name='进货编号')
    productObj = models.ForeignKey(ProductInfo,  db_column='productObj', on_delete=models.PROTECT, verbose_name='进货产品')
    buyDate = models.CharField(max_length=20, default='', verbose_name='进货日期')
    price = models.CharField(max_length=20, default='', verbose_name='进货单价')
    count = models.IntegerField(default=0,verbose_name='进货数量')
    supplyerObj = models.ForeignKey(Supplyer,  db_column='supplyerObj', on_delete=models.PROTECT, verbose_name='供应商')
    personName = models.CharField(max_length=20, default='', verbose_name='负责人')

    class Meta:
        db_table = 't_BuyInfo'
        verbose_name = '产品进货信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        buyInfo = {
            'buyId': self.buyId,
            'productObj': self.productObj.productName,
            'productObjPri': self.productObj.productNo,
            'buyDate': self.buyDate,
            'price': self.price,
            'count': self.count,
            'supplyerObj': self.supplyerObj.supplyerName,
            'supplyerObjPri': self.supplyerObj.supplyerId,
            'personName': self.personName,
        }
        return buyInfo

