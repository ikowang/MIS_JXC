var buyInfo_manage_tool = null; 
$(function () { 
	initBuyInfoManageTool(); //建立BuyInfo管理对象
	buyInfo_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#buyInfo_manage").datagrid({
		url : '/BuyInfo/list',
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
		sortName : "buyId",
		sortOrder : "desc",
		toolbar : "#buyInfo_manage_tool",
		columns : [[
			{
				field : "buyId",
				title : "进货编号",
				width : 70,
			},
			{
				field : "productObj",
				title : "进货产品",
				width : 140,
			},
			{
				field : "buyDate",
				title : "进货日期",
				width : 140,
			},
			{
				field : "price",
				title : "进货单价",
				width : 140,
			},
			{
				field : "count",
				title : "进货数量",
				width : 70,
			},
			{
				field : "supplyerObj",
				title : "供应商",
				width : 140,
			},
			{
				field : "personName",
				title : "负责人",
				width : 140,
			},
		]],
	});

	$("#buyInfoEditDiv").dialog({
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
				if ($("#buyInfoEditForm").form("validate")) {
					//验证表单 
					if(!$("#buyInfoEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#buyInfoEditForm").form({
						    url:"/BuyInfo/update/" + $("#buyInfo_buyId_edit").val(),
						    onSubmit: function(){
								if($("#buyInfoEditForm").form("validate"))  {
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
			                        $("#buyInfoEditDiv").dialog("close");
			                        buyInfo_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#buyInfoEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#buyInfoEditDiv").dialog("close");
				$("#buyInfoEditForm").form("reset"); 
			},
		}],
	});
});

function initBuyInfoManageTool() {
	buyInfo_manage_tool = {
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
				url : "/Supplyer/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#supplyerObj_supplyerId_query").combobox({ 
					    valueField:"supplyerId",
					    textField:"supplyerName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{supplyerId:0,supplyerName:"不限制"});
					$("#supplyerObj_supplyerId_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#buyInfo_manage").datagrid("reload");
		},
		redo : function () {
			$("#buyInfo_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#buyInfo_manage").datagrid("options").queryParams;
			queryParams["productObj.productNo"] = $("#productObj_productNo_query").combobox("getValue");
			queryParams["buyDate"] = $("#buyDate").datebox("getValue"); 
			queryParams["supplyerObj.supplyerId"] = $("#supplyerObj_supplyerId_query").combobox("getValue");
			queryParams["personName"] = $("#personName").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#buyInfo_manage").datagrid("options").queryParams=queryParams; 
			$("#buyInfo_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#buyInfoQueryForm").form({
			    url:"/BuyInfo/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#buyInfoQueryForm").submit();
		},
		remove : function () {
			var rows = $("#buyInfo_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var buyIds = [];
						for (var i = 0; i < rows.length; i ++) {
							buyIds.push(rows[i].buyId);
						}
						$.ajax({
							type : "POST",
							url : "/BuyInfo/deletes",
							data : {
								buyIds : buyIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#buyInfo_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#buyInfo_manage").datagrid("loaded");
									$("#buyInfo_manage").datagrid("load");
									$("#buyInfo_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#buyInfo_manage").datagrid("loaded");
									$("#buyInfo_manage").datagrid("load");
									$("#buyInfo_manage").datagrid("unselectAll");
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
			var rows = $("#buyInfo_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/BuyInfo/update/" + rows[0].buyId,
					type : "get",
					data : {
						//buyId : rows[0].buyId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (buyInfo, response, status) {
						$.messager.progress("close");
						if (buyInfo) { 
							$("#buyInfoEditDiv").dialog("open");
							$("#buyInfo_buyId_edit").val(buyInfo.buyId);
							$("#buyInfo_buyId_edit").validatebox({
								required : true,
								missingMessage : "请输入进货编号",
								editable: false
							});
							$("#buyInfo_productObj_productNo_edit").combobox({
								url:"/ProductInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"productNo",
							    textField:"productName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#buyInfo_productObj_productNo_edit").combobox("select", buyInfo.productObjPri);
									//var data = $("#buyInfo_productObj_productNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#buyInfo_productObj_productNo_edit").combobox("select", data[0].productNo);
						            //}
								}
							});
							$("#buyInfo_buyDate_edit").datebox({
								value: buyInfo.buyDate,
							    required: true,
							    showSeconds: true,
							});
							$("#buyInfo_price_edit").val(buyInfo.price);
							$("#buyInfo_price_edit").validatebox({
								required : true,
								missingMessage : "请输入进货单价",
							});
							$("#buyInfo_count_edit").val(buyInfo.count);
							$("#buyInfo_count_edit").validatebox({
								required : true,
								validType : "integer",
								missingMessage : "请输入进货数量",
								invalidMessage : "进货数量输入不对",
							});
							$("#buyInfo_supplyerObj_supplyerId_edit").combobox({
								url:"/Supplyer/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"supplyerId",
							    textField:"supplyerName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#buyInfo_supplyerObj_supplyerId_edit").combobox("select", buyInfo.supplyerObjPri);
									//var data = $("#buyInfo_supplyerObj_supplyerId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#buyInfo_supplyerObj_supplyerId_edit").combobox("select", data[0].supplyerId);
						            //}
								}
							});
							$("#buyInfo_personName_edit").val(buyInfo.personName);
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
