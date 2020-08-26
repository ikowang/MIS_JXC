from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.SellInfo.models import SellInfo
from apps.CustomerInfo.models import CustomerInfo
from apps.ProductInfo.models import ProductInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台产品销售添加
    def get(self,request):
        customerInfos = CustomerInfo.objects.all()  # 获取所有客户信息
        productInfos = ProductInfo.objects.all()  # 获取所有产品信息
        context = {
            'customerInfos': customerInfos,
            'productInfos': productInfos,
        }

        # 使用模板
        return render(request, 'SellInfo/sellInfo_frontAdd.html', context)

    def post(self, request):
        sellInfo = SellInfo() # 新建一个产品销售对象然后获取参数
        sellInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('sellInfo.productObj.productNo'))
        sellInfo.sellDate = request.POST.get('sellInfo.sellDate')
        sellInfo.price = float(request.POST.get('sellInfo.price'))
        sellInfo.count = int(request.POST.get('sellInfo.count'))
        sellInfo.customerObj = CustomerInfo.objects.get(customerId=request.POST.get('sellInfo.customerObj.customerId'))
        sellInfo.personName = request.POST.get('sellInfo.personName')
        sellInfo.save() # 保存产品销售信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改产品销售
    def get(self, request, sellId):
        context = {'sellId': sellId}
        return render(request, 'SellInfo/sellInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台产品销售查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        sellDate = self.getStrParam(request, 'sellDate')
        customerObj_customerId = self.getIntParam(request, 'customerObj.customerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        sellInfos = SellInfo.objects.all()
        if productObj_productNo != '':
            sellInfos = sellInfos.filter(productObj=productObj_productNo)
        if sellDate != '':
            sellInfos = sellInfos.filter(sellDate__contains=sellDate)
        if customerObj_customerId != '0':
            sellInfos = sellInfos.filter(customerObj=customerObj_customerId)
        if personName != '':
            sellInfos = sellInfos.filter(personName__contains=personName)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(sellInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        sellInfos_page = self.paginator.page(self.currentPage)

        # 获取所有客户信息
        customerInfos = CustomerInfo.objects.all()
        # 获取所有产品信息
        productInfos = ProductInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'customerInfos': customerInfos,
            'productInfos': productInfos,
            'sellInfos_page': sellInfos_page,
            'productObj_productNo': productObj_productNo,
            'sellDate': sellDate,
            'customerObj_customerId': int(customerObj_customerId),
            'personName': personName,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'SellInfo/sellInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示产品销售详情页
    def get(self, request, sellId):
        # 查询需要显示的产品销售对象
        sellInfo = SellInfo.objects.get(sellId=sellId)
        context = {
            'sellInfo': sellInfo
        }
        # 渲染模板显示
        return render(request, 'SellInfo/sellInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有产品销售
    def get(self,request):
        sellInfos = SellInfo.objects.all()
        sellInfoList = []
        for sellInfo in sellInfos:
            sellInfoObj = {
                'sellId': sellInfo.sellId,
            }
            sellInfoList.append(sellInfoObj)
        return JsonResponse(sellInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式产品销售更新
    def get(self, request, sellId):
        # GET方式请求查询产品销售对象并返回产品销售json格式
        sellInfo = SellInfo.objects.get(sellId=sellId)
        return JsonResponse(sellInfo.getJsonObj())

    def post(self, request, sellId):
        # POST方式提交产品销售修改信息更新到数据库
        sellInfo = SellInfo.objects.get(sellId=sellId)
        sellInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('sellInfo.productObj.productNo'))
        sellInfo.sellDate = request.POST.get('sellInfo.sellDate')
        sellInfo.price = float(request.POST.get('sellInfo.price'))
        sellInfo.count = int(request.POST.get('sellInfo.count'))
        sellInfo.customerObj = CustomerInfo.objects.get(customerId=request.POST.get('sellInfo.customerObj.customerId'))
        sellInfo.personName = request.POST.get('sellInfo.personName')
        sellInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台产品销售添加
    def get(self,request):
        customerInfos = CustomerInfo.objects.all()  # 获取所有客户信息
        productInfos = ProductInfo.objects.all()  # 获取所有产品信息
        context = {
            'customerInfos': customerInfos,
            'productInfos': productInfos,
        }

        # 渲染显示模板界面
        return render(request, 'SellInfo/sellInfo_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        sellInfo = SellInfo() # 新建一个产品销售对象然后获取参数
        sellInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('sellInfo.productObj.productNo'))
        sellInfo.sellDate = request.POST.get('sellInfo.sellDate')
        sellInfo.price = float(request.POST.get('sellInfo.price'))
        sellInfo.count = int(request.POST.get('sellInfo.count'))
        sellInfo.customerObj = CustomerInfo.objects.get(customerId=request.POST.get('sellInfo.customerObj.customerId'))
        sellInfo.personName = request.POST.get('sellInfo.personName')
        sellInfo.save() # 保存产品销售信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新产品销售
    def get(self, request, sellId):
        context = {'sellId': sellId}
        return render(request, 'SellInfo/sellInfo_modify.html', context)


class ListView(BaseView):  # 后台产品销售列表
    def get(self, request):
        # 使用模板
        return render(request, 'SellInfo/sellInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        sellDate = self.getStrParam(request, 'sellDate')
        customerObj_customerId = self.getIntParam(request, 'customerObj.customerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        sellInfos = SellInfo.objects.all()
        if productObj_productNo != '':
            sellInfos = sellInfos.filter(productObj=productObj_productNo)
        if sellDate != '':
            sellInfos = sellInfos.filter(sellDate__contains=sellDate)
        if customerObj_customerId != '0':
            sellInfos = sellInfos.filter(customerObj=customerObj_customerId)
        if personName != '':
            sellInfos = sellInfos.filter(personName__contains=personName)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(sellInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        sellInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        sellInfoList = []
        for sellInfo in sellInfos_page:
            sellInfo = sellInfo.getJsonObj()
            sellInfoList.append(sellInfo)
        # 构造模板页面需要的参数
        sellInfo_res = {
            'rows': sellInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(sellInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除产品销售信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        sellIds = self.getStrParam(request, 'sellIds')
        sellIds = sellIds.split(',')
        count = 0
        try:
            for sellId in sellIds:
                SellInfo.objects.get(sellId=sellId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出产品销售信息到excel并下载
    def get(self, request):
        # 收集查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        sellDate = self.getStrParam(request, 'sellDate')
        customerObj_customerId = self.getIntParam(request, 'customerObj.customerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        sellInfos = SellInfo.objects.all()
        if productObj_productNo != '':
            sellInfos = sellInfos.filter(productObj=productObj_productNo)
        if sellDate != '':
            sellInfos = sellInfos.filter(sellDate__contains=sellDate)
        if customerObj_customerId != '0':
            sellInfos = sellInfos.filter(customerObj=customerObj_customerId)
        if personName != '':
            sellInfos = sellInfos.filter(personName__contains=personName)
        #将查询结果集转换成列表
        sellInfoList = []
        for sellInfo in sellInfos:
            sellInfo = sellInfo.getJsonObj()
            sellInfoList.append(sellInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(sellInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'sellId': '销售编号',
            'productObj': '销售产品',
            'sellDate': '销售日期',
            'price': '销售价格',
            'count': '销售数量',
            'customerObj': '销售客户',
            'personName': '销售负责人',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'sellInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="sellInfos.xlsx"'
        return response

