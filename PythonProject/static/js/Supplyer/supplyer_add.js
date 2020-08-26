$(function () {
	$("#supplyer_supplyerName").validatebox({
		required : true, 
		missingMessage : '请输入供应商名称',
	});

	$("#supplyer_telephone").validatebox({
		required : true, 
		missingMessage : '请输入供应商电话',
	});

	$("#supplyer_personName").validatebox({
		required : true, 
		missingMessage : '请输入联系人',
	});

	//单击添加按钮
	$("#supplyerAddButton").click(function () {
		//验证表单 
		if(!$("#supplyerAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#supplyerAddForm").form({
			    url:"/Supplyer/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#supplyerAddForm").form("validate"))  { 
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
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#supplyerAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#supplyerAddForm").submit();
		}
	});

	//单击清空按钮
	$("#supplyerClearButton").click(function () { 
		//$("#supplyerAddForm").form("clear"); 
		location.reload()
	});
});
