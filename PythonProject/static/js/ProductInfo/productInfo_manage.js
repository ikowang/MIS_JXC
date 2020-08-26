var productInfo_manage_tool = null; 
$(function () { 
	initProductInfoManageTool(); //建立ProductInfo管理对象
	productInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#productInfo_manage").datagrid({
		url : '/ProductInfo/list',
		queryParams: {
			"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
		},
		fit : true,
		fitColumns : true,
		striped : true,
		rownumbers : true,
		border : false,
		pagination : true,
		pageSize : 5,
		pageList : [5, 10, 15, 20, 25],
		pageNumber : 1,
		sortName : "productNo",
		sortOrder : "desc",
		toolbar : "#productInfo_manage_tool",
		columns : [[
			{
				field : "productNo",
				title : "产品编号",
				width : 140,
			},
			{
				field : "productClass",
				title : "产品类别",
				width : 140,
			},
			{
				field : "productName",
				title : "产品名称",
				width : 140,
			},
			{
				field : "productPhoto",
				title : "产品图片",
				width : "70px",
				height: "65px",
				formatter: function(val,row) {
					return "<img src='" + val + "' width='65px' height='55px' />";
				}
 			},
			{
				field : "price",
				title : "产品单价",
				width : 70,
			},
			{
				field : "leftCount",
				title : "产品库存",
				width : 70,
			},
			{
				field : "madeDate",
				title : "生产日期",
				width : 140,
			},
		]],
	});

	$("#productInfoEditDiv").dialog({
		title : "修改管理",
		top: "10px",
		width : 1000,
		height : 600,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#productInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#productInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#productInfoEditForm").form({
						    url:"/ProductInfo/update/" + $("#productInfo_productNo_edit").val(),
						    onSubmit: function(){
								if($("#productInfoEditForm").form("validate"))  {
				                	$.messager.progress({
										text : "正在提交数据中...",
									});
				                	return true;
				                } else { 
				                    return false; 
				                }
						    },
						    success:function(data){
						    	$.messager.progress("close");
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#productInfoEditDiv").dialog("close");
			                        productInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#productInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#productInfoEditDiv").dialog("close");
				$("#productInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initProductInfoManageTool() {
	productInfo_manage_tool = {
		init: function() {
			$.ajax({
				url : "/ProductClass/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#productClass_productClassId_query").combobox({ 
					    valueField:"productClassId",
					    textField:"productClassName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{productClassId:0,productClassName:"不限制"});
					$("#productClass_productClassId_query").combobox("loadData",data); 
				}
			});
			//实例化编辑器
			tinyMCE.init({
				selector: "#productInfo_productDesc_edit",
				theme: 'advanced',
				language: "zh",
				strict_loading_mode: 1,
			});
		},
		reload : function () {
			$("#productInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#productInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#productInfo_manage").datagrid("options").queryParams;
			queryParams["productNo"] = $("#productNo").val();
			queryParams["productClass.productClassId"] = $("#productClass_productClassId_query").combobox("getValue");
			queryParams["productName"] = $("#productName").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#productInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#productInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#productInfoQueryForm").form({
			    url:"/ProductInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#productInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#productInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var productNos = [];
						for (var i = 0; i < rows.length; i ++) {
							productNos.push(rows[i].productNo);
						}
						$.ajax({
							type : "POST",
							url : "/ProductInfo/deletes",
							data : {
								productNos : productNos.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#productInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#productInfo_manage").datagrid("loaded");
									$("#productInfo_manage").datagrid("load");
									$("#productInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#productInfo_manage").datagrid("loaded");
									$("#productInfo_manage").datagrid("load");
									$("#productInfo_manage").datagrid("unselectAll");
									$.messager.alert("消息",data.message);
								}
							},
						});
					}
				});
			} else {
				$.messager.alert("提示", "请选择要删除的记录！", "info");
			}
		},
		edit : function () {
			var rows = $("#productInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/ProductInfo/update/" + rows[0].productNo,
					type : "get",
					data : {
						//productNo : rows[0].productNo,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (productInfo, response, status) {
						$.messager.progress("close");
						if (productInfo) { 
							$("#productInfoEditDiv").dialog("open");
							$("#productInfo_productNo_edit").val(productInfo.productNo);
							$("#productInfo_productNo_edit").validatebox({
								required : true,
								missingMessage : "请输入产品编号",
								editable: false
							});
							$("#productInfo_productClass_productClassId_edit").combobox({
								url:"/ProductClass/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"productClassId",
							    textField:"productClassName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#productInfo_productClass_productClassId_edit").combobox("select", productInfo.productClassPri);
									//var data = $("#productInfo_productClass_productClassId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#productInfo_productClass_productClassId_edit").combobox("select", data[0].productClassId);
						            //}
								}
							});
							$("#productInfo_productName_edit").val(productInfo.productName);
							$("#productInfo_productName_edit").validatebox({
								required : true,
								missingMessage : "请输入产品名称",
							});
							$("#productInfo_productPhotoImg").attr("src", productInfo.productPhoto);
							$("#productInfo_price_edit").val(productInfo.price);
							$("#productInfo_price_edit").validatebox({
								required : true,
								validType : "number",
								missingMessage : "请输入产品单价",
								invalidMessage : "产品单价输入不对",
							});
							$("#productInfo_leftCount_edit").val(productInfo.leftCount);
							$("#productInfo_leftCount_edit").validatebox({
								required : true,
								validType : "integer",
								missingMessage : "请输入产品库存",
								invalidMessage : "产品库存输入不对",
							});
							$("#productInfo_madeDate_edit").datebox({
								value: productInfo.madeDate,
							    required: true,
							    showSeconds: true,
							});
							tinyMCE.editors['productInfo_productDesc_edit'].setContent(productInfo.productDesc);
						} else {
							$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
						}
					}
				});
			} else if (rows.length == 0) {
				$.messager.alert("警告操作！", "编辑记录至少选定一条数据！", "warning");
			}
		},
	};
}
