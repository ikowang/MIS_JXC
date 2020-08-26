var sellInfo_manage_tool = null; 
$(function () { 
	initSellInfoManageTool(); //建立SellInfo管理对象
	sellInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#sellInfo_manage").datagrid({
		url : '/SellInfo/list',
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
		sortName : "sellId",
		sortOrder : "desc",
		toolbar : "#sellInfo_manage_tool",
		columns : [[
			{
				field : "sellId",
				title : "销售编号",
				width : 70,
			},
			{
				field : "productObj",
				title : "销售产品",
				width : 140,
			},
			{
				field : "sellDate",
				title : "销售日期",
				width : 140,
			},
			{
				field : "price",
				title : "销售价格",
				width : 70,
			},
			{
				field : "count",
				title : "销售数量",
				width : 70,
			},
			{
				field : "customerObj",
				title : "销售客户",
				width : 140,
			},
			{
				field : "personName",
				title : "销售负责人",
				width : 140,
			},
		]],
	});

	$("#sellInfoEditDiv").dialog({
		title : "修改管理",
		top: "50px",
		width : 700,
		height : 515,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#sellInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#sellInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#sellInfoEditForm").form({
						    url:"/SellInfo/update/" + $("#sellInfo_sellId_edit").val(),
						    onSubmit: function(){
								if($("#sellInfoEditForm").form("validate"))  {
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
			                        $("#sellInfoEditDiv").dialog("close");
			                        sellInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#sellInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#sellInfoEditDiv").dialog("close");
				$("#sellInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initSellInfoManageTool() {
	sellInfo_manage_tool = {
		init: function() {
			$.ajax({
				url : "/ProductInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#productObj_productNo_query").combobox({ 
					    valueField:"productNo",
					    textField:"productName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{productNo:"",productName:"不限制"});
					$("#productObj_productNo_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/CustomerInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#customerObj_customerId_query").combobox({ 
					    valueField:"customerId",
					    textField:"customerName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{customerId:0,customerName:"不限制"});
					$("#customerObj_customerId_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#sellInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#sellInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#sellInfo_manage").datagrid("options").queryParams;
			queryParams["productObj.productNo"] = $("#productObj_productNo_query").combobox("getValue");
			queryParams["sellDate"] = $("#sellDate").datebox("getValue"); 
			queryParams["customerObj.customerId"] = $("#customerObj_customerId_query").combobox("getValue");
			queryParams["personName"] = $("#personName").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#sellInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#sellInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#sellInfoQueryForm").form({
			    url:"/SellInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#sellInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#sellInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var sellIds = [];
						for (var i = 0; i < rows.length; i ++) {
							sellIds.push(rows[i].sellId);
						}
						$.ajax({
							type : "POST",
							url : "/SellInfo/deletes",
							data : {
								sellIds : sellIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#sellInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#sellInfo_manage").datagrid("loaded");
									$("#sellInfo_manage").datagrid("load");
									$("#sellInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#sellInfo_manage").datagrid("loaded");
									$("#sellInfo_manage").datagrid("load");
									$("#sellInfo_manage").datagrid("unselectAll");
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
			var rows = $("#sellInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/SellInfo/update/" + rows[0].sellId,
					type : "get",
					data : {
						//sellId : rows[0].sellId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (sellInfo, response, status) {
						$.messager.progress("close");
						if (sellInfo) { 
							$("#sellInfoEditDiv").dialog("open");
							$("#sellInfo_sellId_edit").val(sellInfo.sellId);
							$("#sellInfo_sellId_edit").validatebox({
								required : true,
								missingMessage : "请输入销售编号",
								editable: false
							});
							$("#sellInfo_productObj_productNo_edit").combobox({
								url:"/ProductInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"productNo",
							    textField:"productName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#sellInfo_productObj_productNo_edit").combobox("select", sellInfo.productObjPri);
									//var data = $("#sellInfo_productObj_productNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#sellInfo_productObj_productNo_edit").combobox("select", data[0].productNo);
						            //}
								}
							});
							$("#sellInfo_sellDate_edit").datebox({
								value: sellInfo.sellDate,
							    required: true,
							    showSeconds: true,
							});
							$("#sellInfo_price_edit").val(sellInfo.price);
							$("#sellInfo_price_edit").validatebox({
								required : true,
								validType : "number",
								missingMessage : "请输入销售价格",
								invalidMessage : "销售价格输入不对",
							});
							$("#sellInfo_count_edit").val(sellInfo.count);
							$("#sellInfo_count_edit").validatebox({
								required : true,
								validType : "integer",
								missingMessage : "请输入销售数量",
								invalidMessage : "销售数量输入不对",
							});
							$("#sellInfo_customerObj_customerId_edit").combobox({
								url:"/CustomerInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"customerId",
							    textField:"customerName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#sellInfo_customerObj_customerId_edit").combobox("select", sellInfo.customerObjPri);
									//var data = $("#sellInfo_customerObj_customerId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#sellInfo_customerObj_customerId_edit").combobox("select", data[0].customerId);
						            //}
								}
							});
							$("#sellInfo_personName_edit").val(sellInfo.personName);
							$("#sellInfo_personName_edit").validatebox({
								required : true,
								missingMessage : "请输入销售负责人",
							});
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
