var supplyer_manage_tool = null; 
$(function () { 
	initSupplyerManageTool(); //建立Supplyer管理对象
	supplyer_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#supplyer_manage").datagrid({
		url : '/Supplyer/list',
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
		sortName : "supplyerId",
		sortOrder : "desc",
		toolbar : "#supplyer_manage_tool",
		columns : [[
			{
				field : "supplyerId",
				title : "供应商编号",
				width : 70,
			},
			{
				field : "supplyerName",
				title : "供应商名称",
				width : 140,
			},
			{
				field : "telephone",
				title : "供应商电话",
				width : 140,
			},
			{
				field : "personName",
				title : "联系人",
				width : 140,
			},
			{
				field : "address",
				title : "供应商地址",
				width : 140,
			},
		]],
	});

	$("#supplyerEditDiv").dialog({
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
				if ($("#supplyerEditForm").form("validate")) {
					//验证表单 
					if(!$("#supplyerEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#supplyerEditForm").form({
						    url:"/Supplyer/update/" + $("#supplyer_supplyerId_edit").val(),
						    onSubmit: function(){
								if($("#supplyerEditForm").form("validate"))  {
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
			                        $("#supplyerEditDiv").dialog("close");
			                        supplyer_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#supplyerEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#supplyerEditDiv").dialog("close");
				$("#supplyerEditForm").form("reset"); 
			},
		}],
	});
});

function initSupplyerManageTool() {
	supplyer_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#supplyer_manage").datagrid("reload");
		},
		redo : function () {
			$("#supplyer_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#supplyer_manage").datagrid("options").queryParams;
			queryParams["supplyerName"] = $("#supplyerName").val();
			queryParams["telephone"] = $("#telephone").val();
			queryParams["personName"] = $("#personName").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#supplyer_manage").datagrid("options").queryParams=queryParams; 
			$("#supplyer_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#supplyerQueryForm").form({
			    url:"/Supplyer/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#supplyerQueryForm").submit();
		},
		remove : function () {
			var rows = $("#supplyer_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var supplyerIds = [];
						for (var i = 0; i < rows.length; i ++) {
							supplyerIds.push(rows[i].supplyerId);
						}
						$.ajax({
							type : "POST",
							url : "/Supplyer/deletes",
							data : {
								supplyerIds : supplyerIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#supplyer_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#supplyer_manage").datagrid("loaded");
									$("#supplyer_manage").datagrid("load");
									$("#supplyer_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#supplyer_manage").datagrid("loaded");
									$("#supplyer_manage").datagrid("load");
									$("#supplyer_manage").datagrid("unselectAll");
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
			var rows = $("#supplyer_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/Supplyer/update/" + rows[0].supplyerId,
					type : "get",
					data : {
						//supplyerId : rows[0].supplyerId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (supplyer, response, status) {
						$.messager.progress("close");
						if (supplyer) { 
							$("#supplyerEditDiv").dialog("open");
							$("#supplyer_supplyerId_edit").val(supplyer.supplyerId);
							$("#supplyer_supplyerId_edit").validatebox({
								required : true,
								missingMessage : "请输入供应商编号",
								editable: false
							});
							$("#supplyer_supplyerName_edit").val(supplyer.supplyerName);
							$("#supplyer_supplyerName_edit").validatebox({
								required : true,
								missingMessage : "请输入供应商名称",
							});
							$("#supplyer_telephone_edit").val(supplyer.telephone);
							$("#supplyer_telephone_edit").validatebox({
								required : true,
								missingMessage : "请输入供应商电话",
							});
							$("#supplyer_personName_edit").val(supplyer.personName);
							$("#supplyer_personName_edit").validatebox({
								required : true,
								missingMessage : "请输入联系人",
							});
							$("#supplyer_address_edit").val(supplyer.address);
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
