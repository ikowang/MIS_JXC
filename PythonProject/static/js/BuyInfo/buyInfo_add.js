$(function () {
	$("#buyInfo_buyDate").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	$("#buyInfo_price").validatebox({
		required : true, 
		missingMessage : '请输入进货单价',
	});

	$("#buyInfo_count").validatebox({
		required : true,
		validType : "integer",
		missingMessage : '请输入进货数量',
		invalidMessage : '进货数量输入不对',
	});

	//单击添加按钮
	$("#buyInfoAddButton").click(function () {
		//验证表单 
		if(!$("#buyInfoAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#buyInfoAddForm").form({
			    url:"/BuyInfo/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#buyInfoAddForm").form("validate"))  { 
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
                        $("#buyInfoAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#buyInfoAddForm").submit();
		}
	});

	//单击清空按钮
	$("#buyInfoClearButton").click(function () { 
		//$("#buyInfoAddForm").form("clear"); 
		location.reload()
	});
});
