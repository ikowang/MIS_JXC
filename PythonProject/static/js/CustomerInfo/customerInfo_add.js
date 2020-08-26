$(function () {
	$("#customerInfo_customerName").validatebox({
		required : true, 
		missingMessage : '请输入客户名称',
	});

	$("#customerInfo_personName").validatebox({
		required : true, 
		missingMessage : '请输入联系人',
	});

	$("#customerInfo_telephone").validatebox({
		required : true, 
		missingMessage : '请输入联系电话',
	});

	//单击添加按钮
	$("#customerInfoAddButton").click(function () {
		//验证表单 
		if(!$("#customerInfoAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#customerInfoAddForm").form({
			    url:"/CustomerInfo/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#customerInfoAddForm").form("validate"))  { 
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
                        $("#customerInfoAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#customerInfoAddForm").submit();
		}
	});

	//单击清空按钮
	$("#customerInfoClearButton").click(function () { 
		//$("#customerInfoAddForm").form("clear"); 
		location.reload()
	});
});
