$(function () {
	//实例化产品描述编辑器
    tinyMCE.init({
        selector: "#productInfo_productDesc",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
	$("#productInfo_productNo").validatebox({
		required : true, 
		missingMessage : '请输入产品编号',
	});

	$("#productInfo_productName").validatebox({
		required : true, 
		missingMessage : '请输入产品名称',
	});

	$("#productInfo_price").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入产品单价',
		invalidMessage : '产品单价输入不对',
	});

	$("#productInfo_leftCount").validatebox({
		required : true,
		validType : "integer",
		missingMessage : '请输入产品库存',
		invalidMessage : '产品库存输入不对',
	});

	$("#productInfo_madeDate").datebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#productInfoAddButton").click(function () {
		if(tinyMCE.editors['productInfo_productDesc'].getContent() == "") {
			alert("请输入产品描述");
			return;
		}
		//验证表单 
		if(!$("#productInfoAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#productInfoAddForm").form({
			    url:"/ProductInfo/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#productInfoAddForm").form("validate"))  { 
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
                        $("#productInfoAddForm").form("clear");
                        tinyMCE.editors['productInfo_productDesc'].setContent("");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#productInfoAddForm").submit();
		}
	});

	//单击清空按钮
	$("#productInfoClearButton").click(function () { 
		//$("#productInfoAddForm").form("clear"); 
		location.reload()
	});
});
