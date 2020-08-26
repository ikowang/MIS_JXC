from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Supplyer.models import Supplyer
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台供应商添加
    def get(self,request):

        # 使用模板
        return render(request, 'Supplyer/supplyer_frontAdd.html')

    def post(self, request):
        supplyer = Supplyer() # 新建一个供应商对象然后获取参数
        supplyer.supplyerName = request.POST.get('supplyer.supplyerName')
        supplyer.telephone = request.POST.get('supplyer.telephone')
        supplyer.personName = request.POST.get('supplyer.personName')
        supplyer.address = request.POST.get('supplyer.address')
        supplyer.save() # 保存供应商信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改供应商
    def get(self, request, supplyerId):
        context = {'supplyerId': supplyerId}
        return render(request, 'Supplyer/supplyer_frontModify.html', context)


class FrontListView(BaseView):  # 前台供应商查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        supplyerName = self.getStrParam(request, 'supplyerName')
        telephone = self.getStrParam(request, 'telephone')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        supplyers = Supplyer.objects.all()
        if supplyerName != '':
            supplyers = supplyers.filter(supplyerName__contains=supplyerName)
        if telephone != '':
            supplyers = supplyers.filter(telephone__contains=telephone)
        if personName != '':
            supplyers = supplyers.filter(personName__contains=personName)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(supplyers, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        supplyers_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'supplyers_page': supplyers_page,
            'supplyerName': supplyerName,
            'telephone': telephone,
            'personName': personName,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Supplyer/supplyer_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示供应商详情页
    def get(self, request, supplyerId):
        # 查询需要显示的供应商对象
        supplyer = Supplyer.objects.get(supplyerId=supplyerId)
        context = {
            'supplyer': supplyer
        }
        # 渲染模板显示
        return render(request, 'Supplyer/supplyer_frontshow.html', context)


class ListAllView(View): # 前台查询所有供应商
    def get(self,request):
        supplyers = Supplyer.objects.all()
        supplyerList = []
        for supplyer in supplyers:
            supplyerObj = {
                'supplyerId': supplyer.supplyerId,
                'supplyerName': supplyer.supplyerName,
            }
            supplyerList.append(supplyerObj)
        return JsonResponse(supplyerList, safe=False)


class UpdateView(BaseView):  # Ajax方式供应商更新
    def get(self, request, supplyerId):
        # GET方式请求查询供应商对象并返回供应商json格式
        supplyer = Supplyer.objects.get(supplyerId=supplyerId)
        return JsonResponse(supplyer.getJsonObj())

    def post(self, request, supplyerId):
        # POST方式提交供应商修改信息更新到数据库
        supplyer = Supplyer.objects.get(supplyerId=supplyerId)
        supplyer.supplyerName = request.POST.get('supplyer.supplyerName')
        supplyer.telephone = request.POST.get('supplyer.telephone')
        supplyer.personName = request.POST.get('supplyer.personName')
        supplyer.address = request.POST.get('supplyer.address')
        supplyer.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台供应商添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'Supplyer/supplyer_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        supplyer = Supplyer() # 新建一个供应商对象然后获取参数
        supplyer.supplyerName = request.POST.get('supplyer.supplyerName')
        supplyer.telephone = request.POST.get('supplyer.telephone')
        supplyer.personName = request.POST.get('supplyer.personName')
        supplyer.address = request.POST.get('supplyer.address')
        supplyer.save() # 保存供应商信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新供应商
    def get(self, request, supplyerId):
        context = {'supplyerId': supplyerId}
        return render(request, 'Supplyer/supplyer_modify.html', context)


class ListView(BaseView):  # 后台供应商列表
    def get(self, request):
        # 使用模板
        return render(request, 'Supplyer/supplyer_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        supplyerName = self.getStrParam(request, 'supplyerName')
        telephone = self.getStrParam(request, 'telephone')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        supplyers = Supplyer.objects.all()
        if supplyerName != '':
            supplyers = supplyers.filter(supplyerName__contains=supplyerName)
        if telephone != '':
            supplyers = supplyers.filter(telephone__contains=telephone)
        if personName != '':
            supplyers = supplyers.filter(personName__contains=personName)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(supplyers, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        supplyers_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        supplyerList = []
        for supplyer in supplyers_page:
            supplyer = supplyer.getJsonObj()
            supplyerList.append(supplyer)
        # 构造模板页面需要的参数
        supplyer_res = {
            'rows': supplyerList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(supplyer_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除供应商信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        supplyerIds = self.getStrParam(request, 'supplyerIds')
        supplyerIds = supplyerIds.split(',')
        count = 0
        try:
            for supplyerId in supplyerIds:
                Supplyer.objects.get(supplyerId=supplyerId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出供应商信息到excel并下载
    def get(self, request):
        # 收集查询参数
        supplyerName = self.getStrParam(request, 'supplyerName')
        telephone = self.getStrParam(request, 'telephone')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        supplyers = Supplyer.objects.all()
        if supplyerName != '':
            supplyers = supplyers.filter(supplyerName__contains=supplyerName)
        if telephone != '':
            supplyers = supplyers.filter(telephone__contains=telephone)
        if personName != '':
            supplyers = supplyers.filter(personName__contains=personName)
        #将查询结果集转换成列表
        supplyerList = []
        for supplyer in supplyers:
            supplyer = supplyer.getJsonObj()
            supplyerList.append(supplyer)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(supplyerList)
        # 设置要导入到excel的列
        columns_map = {
            'supplyerId': '供应商编号',
            'supplyerName': '供应商名称',
            'telephone': '供应商电话',
            'personName': '联系人',
            'address': '供应商地址',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'supplyers.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="supplyers.xlsx"'
        return response

