from django.db import models


class ProductClass(models.Model):
    productClassId = models.AutoField(primary_key=True, verbose_name='商品类别编号')
    productClassName = models.CharField(max_length=20, default='', verbose_name='商品类别名称')

    class Meta:
        db_table = 't_ProductClass'
        verbose_name = '商品类别信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        productClass = {
            'productClassId': self.productClassId,
            'productClassName': self.productClassName,
        }
        return productClass

