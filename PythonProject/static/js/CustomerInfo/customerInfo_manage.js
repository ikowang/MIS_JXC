var customerInfo_manage_tool = null; 
$(function () { 
	initCustomerInfoManageTool(); //建立CustomerInfo管理对象
	customerInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#customerInfo_manage").datagrid({
		url : '/CustomerInfo/list',
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
		sortName : "customerId",
		sortOrder : "desc",
		toolbar : "#customerInfo_manage_tool",
		columns : [[
			{
				field : "customerId",
				title : "客户编号",
				width : 70,
			},
			{
				field : "customerName",
				title : "客户名称",
				width : 140,
			},
			{
				field : "personName",
				title : "联系人",
				width : 140,
			},
			{
				field : "telephone",
				title : "联系电话",
				width : 140,
			},
			{
				field : "address",
				title : "联系地址",
				width : 140,
			},
		]],
	});

	$("#customerInfoEditDiv").dialog({
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
				if ($("#customerInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#customerInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#customerInfoEditForm").form({
						    url:"/CustomerInfo/update/" + $("#customerInfo_customerId_edit").val(),
						    onSubmit: function(){
								if($("#customerInfoEditForm").form("validate"))  {
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
			                        $("#customerInfoEditDiv").dialog("close");
			                        customerInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#customerInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#customerInfoEditDiv").dialog("close");
				$("#customerInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initCustomerInfoManageTool() {
	customerInfo_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#customerInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#customerInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#customerInfo_manage").datagrid("options").queryParams;
			queryParams["customerName"] = $("#customerName").val();
			queryParams["personName"] = $("#personName").val();
			queryParams["telephone"] = $("#telephone").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#customerInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#customerInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#customerInfoQueryForm").form({
			    url:"/CustomerInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#customerInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#customerInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var customerIds = [];
						for (var i = 0; i < rows.length; i ++) {
							customerIds.push(rows[i].customerId);
						}
						$.ajax({
							type : "POST",
							url : "/CustomerInfo/deletes",
							data : {
								customerIds : customerIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#customerInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#customerInfo_manage").datagrid("loaded");
									$("#customerInfo_manage").datagrid("load");
									$("#customerInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#customerInfo_manage").datagrid("loaded");
									$("#customerInfo_manage").datagrid("load");
									$("#customerInfo_manage").datagrid("unselectAll");
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
			var rows = $("#customerInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/CustomerInfo/update/" + rows[0].customerId,
					type : "get",
					data : {
						//customerId : rows[0].customerId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (customerInfo, response, status) {
						$.messager.progress("close");
						if (customerInfo) { 
							$("#customerInfoEditDiv").dialog("open");
							$("#customerInfo_customerId_edit").val(customerInfo.customerId);
							$("#customerInfo_customerId_edit").validatebox({
								required : true,
								missingMessage : "请输入客户编号",
								editable: false
							});
							$("#customerInfo_customerName_edit").val(customerInfo.customerName);
							$("#customerInfo_customerName_edit").validatebox({
								required : true,
								missingMessage : "请输入客户名称",
							});
							$("#customerInfo_personName_edit").val(customerInfo.personName);
							$("#customerInfo_personName_edit").validatebox({
								required : true,
								missingMessage : "请输入联系人",
							});
							$("#customerInfo_telephone_edit").val(customerInfo.telephone);
							$("#customerInfo_telephone_edit").validatebox({
								required : true,
								missingMessage : "请输入联系电话",
							});
							$("#customerInfo_address_edit").val(customerInfo.address);
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
