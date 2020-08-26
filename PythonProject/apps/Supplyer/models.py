from django.db import models


class Supplyer(models.Model):
    supplyerId = models.AutoField(primary_key=True, verbose_name='供应商编号')
    supplyerName = models.CharField(max_length=20, default='', verbose_name='供应商名称')
    telephone = models.CharField(max_length=20, default='', verbose_name='供应商电话')
    personName = models.CharField(max_length=20, default='', verbose_name='联系人')
    address = models.CharField(max_length=20, default='', verbose_name='供应商地址')

    class Meta:
        db_table = 't_Supplyer'
        verbose_name = '供应商信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        supplyer = {
            'supplyerId': self.supplyerId,
            'supplyerName': self.supplyerName,
            'telephone': self.telephone,
            'personName': self.personName,
            'address': self.address,
        }
        return supplyer

