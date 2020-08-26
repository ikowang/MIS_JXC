from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.BuyInfo.models import BuyInfo
from apps.ProductInfo.models import ProductInfo
from apps.Supplyer.models import Supplyer
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台产品进货添加
    def get(self,request):
        productInfos = ProductInfo.objects.all()  # 获取所有产品信息
        supplyers = Supplyer.objects.all()  # 获取所有供应商
        context = {
            'productInfos': productInfos,
            'supplyers': supplyers,
        }

        # 使用模板
        return render(request, 'BuyInfo/buyInfo_frontAdd.html', context)

    def post(self, request):
        buyInfo = BuyInfo() # 新建一个产品进货对象然后获取参数
        buyInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('buyInfo.productObj.productNo'))
        buyInfo.buyDate = request.POST.get('buyInfo.buyDate')
        buyInfo.price = request.POST.get('buyInfo.price')
        buyInfo.count = int(request.POST.get('buyInfo.count'))
        buyInfo.supplyerObj = Supplyer.objects.get(supplyerId=request.POST.get('buyInfo.supplyerObj.supplyerId'))
        buyInfo.personName = request.POST.get('buyInfo.personName')
        buyInfo.save() # 保存产品进货信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改产品进货
    def get(self, request, buyId):
        context = {'buyId': buyId}
        return render(request, 'BuyInfo/buyInfo_frontModify.html', context)


class FrontListView(BaseView):  # 前台产品进货查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        buyDate = self.getStrParam(request, 'buyDate')
        supplyerObj_supplyerId = self.getIntParam(request, 'supplyerObj.supplyerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        buyInfos = BuyInfo.objects.all()
        if productObj_productNo != '':
            buyInfos = buyInfos.filter(productObj=productObj_productNo)
        if buyDate != '':
            buyInfos = buyInfos.filter(buyDate__contains=buyDate)
        if supplyerObj_supplyerId != '0':
            buyInfos = buyInfos.filter(supplyerObj=supplyerObj_supplyerId)
        if personName != '':
            buyInfos = buyInfos.filter(personName__contains=personName)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(buyInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        buyInfos_page = self.paginator.page(self.currentPage)

        # 获取所有产品信息
        productInfos = ProductInfo.objects.all()
        # 获取所有供应商
        supplyers = Supplyer.objects.all()
        # 构造模板需要的参数
        context = {
            'productInfos': productInfos,
            'supplyers': supplyers,
            'buyInfos_page': buyInfos_page,
            'productObj_productNo': productObj_productNo,
            'buyDate': buyDate,
            'supplyerObj_supplyerId': int(supplyerObj_supplyerId),
            'personName': personName,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'BuyInfo/buyInfo_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示产品进货详情页
    def get(self, request, buyId):
        # 查询需要显示的产品进货对象
        buyInfo = BuyInfo.objects.get(buyId=buyId)
        context = {
            'buyInfo': buyInfo
        }
        # 渲染模板显示
        return render(request, 'BuyInfo/buyInfo_frontshow.html', context)


class ListAllView(View): # 前台查询所有产品进货
    def get(self,request):
        buyInfos = BuyInfo.objects.all()
        buyInfoList = []
        for buyInfo in buyInfos:
            buyInfoObj = {
                'buyId': buyInfo.buyId,
            }
            buyInfoList.append(buyInfoObj)
        return JsonResponse(buyInfoList, safe=False)


class UpdateView(BaseView):  # Ajax方式产品进货更新
    def get(self, request, buyId):
        # GET方式请求查询产品进货对象并返回产品进货json格式
        buyInfo = BuyInfo.objects.get(buyId=buyId)
        return JsonResponse(buyInfo.getJsonObj())

    def post(self, request, buyId):
        # POST方式提交产品进货修改信息更新到数据库
        buyInfo = BuyInfo.objects.get(buyId=buyId)
        buyInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('buyInfo.productObj.productNo'))
        buyInfo.buyDate = request.POST.get('buyInfo.buyDate')
        buyInfo.price = request.POST.get('buyInfo.price')
        buyInfo.count = int(request.POST.get('buyInfo.count'))
        buyInfo.supplyerObj = Supplyer.objects.get(supplyerId=request.POST.get('buyInfo.supplyerObj.supplyerId'))
        buyInfo.personName = request.POST.get('buyInfo.personName')
        buyInfo.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台产品进货添加
    def get(self,request):
        productInfos = ProductInfo.objects.all()  # 获取所有产品信息
        supplyers = Supplyer.objects.all()  # 获取所有供应商
        context = {
            'productInfos': productInfos,
            'supplyers': supplyers,
        }

        # 渲染显示模板界面
        return render(request, 'BuyInfo/buyInfo_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        buyInfo = BuyInfo() # 新建一个产品进货对象然后获取参数
        buyInfo.productObj = ProductInfo.objects.get(productNo=request.POST.get('buyInfo.productObj.productNo'))
        buyInfo.buyDate = request.POST.get('buyInfo.buyDate')
        buyInfo.price = request.POST.get('buyInfo.price')
        buyInfo.count = int(request.POST.get('buyInfo.count'))
        buyInfo.supplyerObj = Supplyer.objects.get(supplyerId=request.POST.get('buyInfo.supplyerObj.supplyerId'))
        buyInfo.personName = request.POST.get('buyInfo.personName')
        buyInfo.save() # 保存产品进货信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新产品进货
    def get(self, request, buyId):
        context = {'buyId': buyId}
        return render(request, 'BuyInfo/buyInfo_modify.html', context)


class ListView(BaseView):  # 后台产品进货列表
    def get(self, request):
        # 使用模板
        return render(request, 'BuyInfo/buyInfo_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        buyDate = self.getStrParam(request, 'buyDate')
        supplyerObj_supplyerId = self.getIntParam(request, 'supplyerObj.supplyerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        buyInfos = BuyInfo.objects.all()
        if productObj_productNo != '':
            buyInfos = buyInfos.filter(productObj=productObj_productNo)
        if buyDate != '':
            buyInfos = buyInfos.filter(buyDate__contains=buyDate)
        if supplyerObj_supplyerId != '0':
            buyInfos = buyInfos.filter(supplyerObj=supplyerObj_supplyerId)
        if personName != '':
            buyInfos = buyInfos.filter(personName__contains=personName)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(buyInfos, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        buyInfos_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        buyInfoList = []
        for buyInfo in buyInfos_page:
            buyInfo = buyInfo.getJsonObj()
            buyInfoList.append(buyInfo)
        # 构造模板页面需要的参数
        buyInfo_res = {
            'rows': buyInfoList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(buyInfo_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除产品进货信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        buyIds = self.getStrParam(request, 'buyIds')
        buyIds = buyIds.split(',')
        count = 0
        try:
            for buyId in buyIds:
                BuyInfo.objects.get(buyId=buyId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出产品进货信息到excel并下载
    def get(self, request):
        # 收集查询参数
        productObj_productNo = self.getStrParam(request, 'productObj.productNo')
        buyDate = self.getStrParam(request, 'buyDate')
        supplyerObj_supplyerId = self.getIntParam(request, 'supplyerObj.supplyerId')
        personName = self.getStrParam(request, 'personName')
        # 然后条件组合查询过滤
        buyInfos = BuyInfo.objects.all()
        if productObj_productNo != '':
            buyInfos = buyInfos.filter(productObj=productObj_productNo)
        if buyDate != '':
            buyInfos = buyInfos.filter(buyDate__contains=buyDate)
        if supplyerObj_supplyerId != '0':
            buyInfos = buyInfos.filter(supplyerObj=supplyerObj_supplyerId)
        if personName != '':
            buyInfos = buyInfos.filter(personName__contains=personName)
        #将查询结果集转换成列表
        buyInfoList = []
        for buyInfo in buyInfos:
            buyInfo = buyInfo.getJsonObj()
            buyInfoList.append(buyInfo)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(buyInfoList)
        # 设置要导入到excel的列
        columns_map = {
            'buyId': '进货编号',
            'productObj': '进货产品',
            'buyDate': '进货日期',
            'price': '进货单价',
            'count': '进货数量',
            'supplyerObj': '供应商',
            'personName': '负责人',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'buyInfos.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="buyInfos.xlsx"'
        return response

