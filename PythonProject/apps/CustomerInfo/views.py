from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.CustomerInfo.models import CustomerInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台客户信息添加
    def get(self,request):

        # 使用模板
        return render(request, 'CustomerInfo/customerInfo_frontAdd.html')

    def post(self, request):
        customerInfo = CustomerInfo() # 新建一个客户信息对象然后获取参数
        customerInfo.customerName = request.POST.get('customerInfo.customerName')
        customerInfo.personName = request.POST.get('customerInfo.personName')
        customerInfo.telephone = request.POST.get('customerInfo.telephone')
        customerInfo.address = request.POST.get('customerInfo.address')
        customerInfo.save() # 保存客户信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改客户信息
    def get(self, request, customerId):
        context = {'customerId': customerId}
        return render(request, 'CustomerInfo/customerInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台客户信息查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        customerName = self.getStrParam(request, 'customerName')
        personName = self.getStrParam(request, 'personName')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        customerInfos = CustomerInfo.objects.all()
        if customerName != '':
            customerInfos = customerInfos.filter(customerName__contains=customerName)
        if personName != '':
            customerInfos = customerInfos.filter(personName__contains=personName)
        if telephone != '':
            customerInfos = customerInfos.filter(telephone__contains=telephone)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(customerInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        customerInfos_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'customerInfos_page': customerInfos_page,
            'customerName': customerName,
            'personName': personName,
            'telephone': telephone,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'CustomerInfo/customerInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示客户信息详情页
    def get(self, request, customerId):
        # 查询需要显示的客户信息对象
        customerInfo = CustomerInfo.objects.get(customerId=customerId)
        context = {
            'customerInfo': customerInfo
        }
        # 渲染模板显示
        return render(request, 'CustomerInfo/customerInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有客户信息
    def get(self,request):
        customerInfos = CustomerInfo.objects.all()
        customerInfoList = []
        for customerInfo in customerInfos:
            customerInfoObj = {
                'customerId': customerInfo.customerId,
                'customerName': customerInfo.customerName,
            }
            customerInfoList.append(customerInfoObj)
        return JsonResponse(customerInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式客户信息更新
    def get(self, request, customerId):
        # GET方式请求查询客户信息对象并返回客户信息json格式
        customerInfo = CustomerInfo.objects.get(customerId=customerId)
        return JsonResponse(customerInfo.getJsonObj())

    def post(self, request, customerId):
        # POST方式提交客户信息修改信息更新到数据库
        customerInfo = CustomerInfo.objects.get(customerId=customerId)
        customerInfo.customerName = request.POST.get('customerInfo.customerName')
        customerInfo.personName = request.POST.get('customerInfo.personName')
        customerInfo.telephone = request.POST.get('customerInfo.telephone')
        customerInfo.address = request.POST.get('customerInfo.address')
        customerInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台客户信息添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'CustomerInfo/customerInfo_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        customerInfo = CustomerInfo() # 新建一个客户信息对象然后获取参数
        customerInfo.customerName = request.POST.get('customerInfo.customerName')
        customerInfo.personName = request.POST.get('customerInfo.personName')
        customerInfo.telephone = request.POST.get('customerInfo.telephone')
        customerInfo.address = request.POST.get('customerInfo.address')
        customerInfo.save() # 保存客户信息信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新客户信息
    def get(self, request, customerId):
        context = {'customerId': customerId}
        return render(request, 'CustomerInfo/customerInfo_modify.html', context)


class ListView(BaseView):  # 后台客户信息列表
    def get(self, request):
        # 使用模板
        return render(request, 'CustomerInfo/customerInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        customerName = self.getStrParam(request, 'customerName')
        personName = self.getStrParam(request, 'personName')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        customerInfos = CustomerInfo.objects.all()
        if customerName != '':
            customerInfos = customerInfos.filter(customerName__contains=customerName)
        if personName != '':
            customerInfos = customerInfos.filter(personName__contains=personName)
        if telephone != '':
            customerInfos = customerInfos.filter(telephone__contains=telephone)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(customerInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        customerInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        customerInfoList = []
        for customerInfo in customerInfos_page:
            customerInfo = customerInfo.getJsonObj()
            customerInfoList.append(customerInfo)
        # 构造模板页面需要的参数
        customerInfo_res = {
            'rows': customerInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(customerInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除客户信息信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        customerIds = self.getStrParam(request, 'customerIds')
        customerIds = customerIds.split(',')
        count = 0
        try:
            for customerId in customerIds:
                CustomerInfo.objects.get(customerId=customerId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出客户信息信息到excel并下载
    def get(self, request):
        # 收集查询参数
        customerName = self.getStrParam(request, 'customerName')
        personName = self.getStrParam(request, 'personName')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        customerInfos = CustomerInfo.objects.all()
        if customerName != '':
            customerInfos = customerInfos.filter(customerName__contains=customerName)
        if personName != '':
            customerInfos = customerInfos.filter(personName__contains=personName)
        if telephone != '':
            customerInfos = customerInfos.filter(telephone__contains=telephone)
        #将查询结果集转换成列表
        customerInfoList = []
        for customerInfo in customerInfos:
            customerInfo = customerInfo.getJsonObj()
            customerInfoList.append(customerInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(customerInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'customerId': '客户编号',
            'customerName': '客户名称',
            'personName': '联系人',
            'telephone': '联系电话',
            'address': '联系地址',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'customerInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="customerInfos.xlsx"'
        return response

