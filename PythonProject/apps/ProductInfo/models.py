from django.db import models
from apps.ProductClass.models import ProductClass
from tinymce.models import HTMLField


class ProductInfo(models.Model):
    productNo = models.CharField(max_length=20, default='', primary_key=True, verbose_name='产品编号')
    productClass = models.ForeignKey(ProductClass,  db_column='productClass', on_delete=models.PROTECT, verbose_name='产品类别')
    productName = models.CharField(max_length=20, default='', verbose_name='产品名称')
    productPhoto = models.ImageField(upload_to='img', max_length='100', verbose_name='产品图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='产品单价')
    leftCount = models.IntegerField(default=0,verbose_name='产品库存')
    madeDate = models.CharField(max_length=20, default='', verbose_name='生产日期')
    productDesc = HTMLField(max_length=8000, verbose_name='产品描述')

    class Meta:
        db_table = 't_ProductInfo'
        verbose_name = '产品信息信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        productInfo = {
            'productNo': self.productNo,
            'productClass': self.productClass.productClassName,
            'productClassPri': self.productClass.productClassId,
            'productName': self.productName,
            'productPhoto': self.productPhoto.url,
            'price': self.price,
            'leftCount': self.leftCount,
            'madeDate': self.madeDate,
            'productDesc': self.productDesc,
        }
        return productInfo

