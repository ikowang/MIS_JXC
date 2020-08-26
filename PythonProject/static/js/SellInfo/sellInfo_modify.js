$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/SellInfo/update/" + $("#sellInfo_sellId_modify").val(),
		type : "get",
		data : {
			//sellId : $("#sellInfo_sellId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (sellInfo, response, status) {
			$.messager.progress("close");
			if (sellInfo) { 
				$("#sellInfo_sellId_modify").val(sellInfo.sellId);
				$("#sellInfo_sellId_modify").validatebox({
					required : true,
					missingMessage : "请输入销售编号",
					editable: false
				});
				$("#sellInfo_productObj_productNo_modify").combobox({
					url:"/ProductInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"productNo",
					textField:"productName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#sellInfo_productObj_productNo_modify").combobox("select", sellInfo.productObjPri);
						//var data = $("#sellInfo_productObj_productNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#sellInfo_productObj_productNo_edit").combobox("select", data[0].productNo);
						//}
					}
				});
				$("#sellInfo_sellDate_modify").datebox({
					value: sellInfo.sellDate,
					required: true,
					showSeconds: true,
				});
				$("#sellInfo_price_modify").val(sellInfo.price);
				$("#sellInfo_price_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入销售价格",
					invalidMessage : "销售价格输入不对",
				});
				$("#sellInfo_count_modify").val(sellInfo.count);
				$("#sellInfo_count_modify").validatebox({
					required : true,
					validType : "integer",
					missingMessage : "请输入销售数量",
					invalidMessage : "销售数量输入不对",
				});
				$("#sellInfo_customerObj_customerId_modify").combobox({
					url:"/CustomerInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"customerId",
					textField:"customerName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#sellInfo_customerObj_customerId_modify").combobox("select", sellInfo.customerObjPri);
						//var data = $("#sellInfo_customerObj_customerId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#sellInfo_customerObj_customerId_edit").combobox("select", data[0].customerId);
						//}
					}
				});
				$("#sellInfo_personName_modify").val(sellInfo.personName);
				$("#sellInfo_personName_modify").validatebox({
					required : true,
					missingMessage : "请输入销售负责人",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#sellInfoModifyButton").click(function(){ 
		if ($("#sellInfoModifyForm").form("validate")) {
			$("#sellInfoModifyForm").form({
			    url:"SellInfo/update/" + $("#sellInfo_sellId_modify").val(),
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#sellInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
