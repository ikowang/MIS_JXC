from django.db import models
from apps.CustomerInfo.models import CustomerInfo
from apps.ProductInfo.models import ProductInfo


class SellInfo(models.Model):
    sellId = models.AutoField(primary_key=True, verbose_name='销售编号')
    productObj = models.ForeignKey(ProductInfo,  db_column='productObj', on_delete=models.PROTECT, verbose_name='销售产品')
    sellDate = models.CharField(max_length=20, default='', verbose_name='销售日期')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='销售价格')
    count = models.IntegerField(default=0,verbose_name='销售数量')
    customerObj = models.ForeignKey(CustomerInfo,  db_column='customerObj', on_delete=models.PROTECT, verbose_name='销售客户')
    personName = models.CharField(max_length=20, default='', verbose_name='销售负责人')

    class Meta:
        db_table = 't_SellInfo'
        verbose_name = '产品销售信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        sellInfo = {
            'sellId': self.sellId,
            'productObj': self.productObj.productName,
            'productObjPri': self.productObj.productNo,
            'sellDate': self.sellDate,
            'price': self.price,
            'count': self.count,
            'customerObj': self.customerObj.customerName,
            'customerObjPri': self.customerObj.customerId,
            'personName': self.personName,
        }
        return sellInfo

