from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ProductInfo.models import ProductInfo
from apps.ProductClass.models import ProductClass
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台产品信息添加
    def primaryKeyExist(self, productNo):  # 判断主键是否存在
        try:
            ProductInfo.objects.get(productNo=productNo)
            return True
        except ProductInfo.DoesNotExist:
            return False

    def get(self,request):
        productClasss = ProductClass.objects.all()  # 获取所有商品类别
        context = {
            'productClasss': productClasss,
        }

        # 使用模板
        return render(request, 'ProductInfo/productInfo_frontAdd.html', context)

    def post(self, request):
        productNo = request.POST.get('productInfo.productNo') # 判断产品编号是否存在
        if self.primaryKeyExist(productNo):
            return JsonResponse({'success': False, 'message': '产品编号已经存在'})

        productInfo = ProductInfo() # 新建一个产品信息对象然后获取参数
        productInfo.productNo = productNo
        productInfo.productClass = ProductClass.objects.get(productClassId=request.POST.get('productInfo.productClass.productClassId'))
        productInfo.productName = request.POST.get('productInfo.productName')
        try:
            productInfo.productPhoto = self.uploadImageFile(request,'productInfo.productPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        productInfo.price = float(request.POST.get('productInfo.price'))
        productInfo.leftCount = int(request.POST.get('productInfo.leftCount'))
        productInfo.madeDate = request.POST.get('productInfo.madeDate')
        productInfo.productDesc = request.POST.get('productInfo.productDesc')
        productInfo.save() # 保存产品信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改产品信息
    def get(self, request, productNo):
        context = {'productNo': productNo}
        return render(request, 'ProductInfo/productInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台产品信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        productNo = self.getStrParam(request, 'productNo')
        productClass_productClassId = self.getIntParam(request, 'productClass.productClassId')
        productName = self.getStrParam(request, 'productName')
        # 然后条件组合查询过滤
        productInfos = ProductInfo.objects.all()
        if productNo != '':
            productInfos = productInfos.filter(productNo__contains=productNo)
        if productClass_productClassId != '0':
            productInfos = productInfos.filter(productClass=productClass_productClassId)
        if productName != '':
            productInfos = productInfos.filter(productName__contains=productName)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(productInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        productInfos_page = self.paginator.page(self.currentPage)

        # 获取所有商品类别
        productClasss = ProductClass.objects.all()
        # 构造模板需要的参数
        context = {
            'productClasss': productClasss,
            'productInfos_page': productInfos_page,
            'productNo': productNo,
            'productClass_productClassId': int(productClass_productClassId),
            'productName': productName,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ProductInfo/productInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示产品信息详情页
    def get(self, request, productNo):
        # 查询需要显示的产品信息对象
        productInfo = ProductInfo.objects.get(productNo=productNo)
        context = {
            'productInfo': productInfo
        }
        # 渲染模板显示
        return render(request, 'ProductInfo/productInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有产品信息
    def get(self,request):
        productInfos = ProductInfo.objects.all()
        productInfoList = []
        for productInfo in productInfos:
            productInfoObj = {
                'productNo': productInfo.productNo,
                'productName': productInfo.productName,
            }
            productInfoList.append(productInfoObj)
        return JsonResponse(productInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式产品信息更新
    def get(self, request, productNo):
        # GET方式请求查询产品信息对象并返回产品信息json格式
        productInfo = ProductInfo.objects.get(productNo=productNo)
        return JsonResponse(productInfo.getJsonObj())

    def post(self, request, productNo):
        # POST方式提交产品信息修改信息更新到数据库
        productInfo = ProductInfo.objects.get(productNo=productNo)
        productInfo.productClass = ProductClass.objects.get(productClassId=request.POST.get('productInfo.productClass.productClassId'))
        productInfo.productName = request.POST.get('productInfo.productName')
        try:
            productPhotoName = self.uploadImageFile(request, 'productInfo.productPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if productPhotoName != 'img/NoImage.jpg':
            productInfo.productPhoto = productPhotoName
        productInfo.price = float(request.POST.get('productInfo.price'))
        productInfo.leftCount = int(request.POST.get('productInfo.leftCount'))
        productInfo.madeDate = request.POST.get('productInfo.madeDate')
        productInfo.productDesc = request.POST.get('productInfo.productDesc')
        productInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台产品信息添加
    def primaryKeyExist(self, productNo):  # 判断主键是否存在
        try:
            ProductInfo.objects.get(productNo=productNo)
            return True
        except ProductInfo.DoesNotExist:
            return False

    def get(self,request):
        productClasss = ProductClass.objects.all()  # 获取所有商品类别
        context = {
            'productClasss': productClasss,
        }

        # 渲染显示模板界面
        return render(request, 'ProductInfo/productInfo_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        productNo = request.POST.get('productInfo.productNo') # 判断产品编号是否存在
        if self.primaryKeyExist(productNo):
            return JsonResponse({'success': False, 'message': '产品编号已经存在'})

        productInfo = ProductInfo() # 新建一个产品信息对象然后获取参数
        productInfo.productNo = productNo
        productInfo.productClass = ProductClass.objects.get(productClassId=request.POST.get('productInfo.productClass.productClassId'))
        productInfo.productName = request.POST.get('productInfo.productName')
        try:
            productInfo.productPhoto = self.uploadImageFile(request,'productInfo.productPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        productInfo.price = float(request.POST.get('productInfo.price'))
        productInfo.leftCount = int(request.POST.get('productInfo.leftCount'))
        productInfo.madeDate = request.POST.get('productInfo.madeDate')
        productInfo.productDesc = request.POST.get('productInfo.productDesc')
        productInfo.save() # 保存产品信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新产品信息
    def get(self, request, productNo):
        context = {'productNo': productNo}
        return render(request, 'ProductInfo/productInfo_modify.html', context)


class ListView(BaseView):  # 后台产品信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'ProductInfo/productInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        productNo = self.getStrParam(request, 'productNo')
        productClass_productClassId = self.getIntParam(request, 'productClass.productClassId')
        productName = self.getStrParam(request, 'productName')
        # 然后条件组合查询过滤
        productInfos = ProductInfo.objects.all()
        if productNo != '':
            productInfos = productInfos.filter(productNo__contains=productNo)
        if productClass_productClassId != '0':
            productInfos = productInfos.filter(productClass=productClass_productClassId)
        if productName != '':
            productInfos = productInfos.filter(productName__contains=productName)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(productInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        productInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        productInfoList = []
        for productInfo in productInfos_page:
            productInfo = productInfo.getJsonObj()
            productInfoList.append(productInfo)
        # 构造模板页面需要的参数
        productInfo_res = {
            'rows': productInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(productInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除产品信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        productNos = self.getStrParam(request, 'productNos')
        productNos = productNos.split(',')
        count = 0
        try:
            for productNo in productNos:
                ProductInfo.objects.get(productNo=productNo).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出产品信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        productNo = self.getStrParam(request, 'productNo')
        productClass_productClassId = self.getIntParam(request, 'productClass.productClassId')
        productName = self.getStrParam(request, 'productName')
        # 然后条件组合查询过滤
        productInfos = ProductInfo.objects.all()
        if productNo != '':
            productInfos = productInfos.filter(productNo__contains=productNo)
        if productClass_productClassId != '0':
            productInfos = productInfos.filter(productClass=productClass_productClassId)
        if productName != '':
            productInfos = productInfos.filter(productName__contains=productName)
        #将查询结果集转换成列表
        productInfoList = []
        for productInfo in productInfos:
            productInfo = productInfo.getJsonObj()
            productInfoList.append(productInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(productInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'productNo': '产品编号',
            'productClass': '产品类别',
            'productName': '产品名称',
            'price': '产品单价',
            'leftCount': '产品库存',
            'madeDate': '生产日期',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'productInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="productInfos.xlsx"'
        return response

