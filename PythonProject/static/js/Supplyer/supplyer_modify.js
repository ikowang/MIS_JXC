$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Supplyer/update/" + $("#supplyer_supplyerId_modify").val(),
		type : "get",
		data : {
			//supplyerId : $("#supplyer_supplyerId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (supplyer, response, status) {
			$.messager.progress("close");
			if (supplyer) { 
				$("#supplyer_supplyerId_modify").val(supplyer.supplyerId);
				$("#supplyer_supplyerId_modify").validatebox({
					required : true,
					missingMessage : "请输入供应商编号",
					editable: false
				});
				$("#supplyer_supplyerName_modify").val(supplyer.supplyerName);
				$("#supplyer_supplyerName_modify").validatebox({
					required : true,
					missingMessage : "请输入供应商名称",
				});
				$("#supplyer_telephone_modify").val(supplyer.telephone);
				$("#supplyer_telephone_modify").validatebox({
					required : true,
					missingMessage : "请输入供应商电话",
				});
				$("#supplyer_personName_modify").val(supplyer.personName);
				$("#supplyer_personName_modify").validatebox({
					required : true,
					missingMessage : "请输入联系人",
				});
				$("#supplyer_address_modify").val(supplyer.address);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#supplyerModifyButton").click(function(){ 
		if ($("#supplyerModifyForm").form("validate")) {
			$("#supplyerModifyForm").form({
			    url:"Supplyer/update/" + $("#supplyer_supplyerId_modify").val(),
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
			$("#supplyerModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
