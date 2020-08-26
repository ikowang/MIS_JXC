from django.db import models


class CustomerInfo(models.Model):
    customerId = models.AutoField(primary_key=True, verbose_name='客户编号')
    customerName = models.CharField(max_length=20, default='', verbose_name='客户名称')
    personName = models.CharField(max_length=20, default='', verbose_name='联系人')
    telephone = models.CharField(max_length=20, default='', verbose_name='联系电话')
    address = models.CharField(max_length=20, default='', verbose_name='联系地址')

    class Meta:
        db_table = 't_CustomerInfo'
        verbose_name = '客户信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        customerInfo = {
            'customerId': self.customerId,
            'customerName': self.customerName,
            'personName': self.personName,
            'telephone': self.telephone,
            'address': self.address,
        }
        return customerInfo

