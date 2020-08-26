$(function () {
    //实例化产品描述编辑器
    tinyMCE.init({
        selector: "#productInfo_productDesc_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ProductInfo/update/" + $("#productInfo_productNo_modify").val(),
		type : "get",
		data : {
			//productNo : $("#productInfo_productNo_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (productInfo, response, status) {
			$.messager.progress("close");
			if (productInfo) { 
				$("#productInfo_productNo_modify").val(productInfo.productNo);
				$("#productInfo_productNo_modify").validatebox({
					required : true,
					missingMessage : "请输入产品编号",
					editable: false
				});
				$("#productInfo_productClass_productClassId_modify").combobox({
					url:"/ProductClass/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"productClassId",
					textField:"productClassName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#productInfo_productClass_productClassId_modify").combobox("select", productInfo.productClassPri);
						//var data = $("#productInfo_productClass_productClassId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#productInfo_productClass_productClassId_edit").combobox("select", data[0].productClassId);
						//}
					}
				});
				$("#productInfo_productName_modify").val(productInfo.productName);
				$("#productInfo_productName_modify").validatebox({
					required : true,
					missingMessage : "请输入产品名称",
				});
				$("#productInfo_productPhotoImgMod").attr("src", productInfo.productPhoto);
				$("#productInfo_price_modify").val(productInfo.price);
				$("#productInfo_price_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入产品单价",
					invalidMessage : "产品单价输入不对",
				});
				$("#productInfo_leftCount_modify").val(productInfo.leftCount);
				$("#productInfo_leftCount_modify").validatebox({
					required : true,
					validType : "integer",
					missingMessage : "请输入产品库存",
					invalidMessage : "产品库存输入不对",
				});
				$("#productInfo_madeDate_modify").datebox({
					value: productInfo.madeDate,
					required: true,
					showSeconds: true,
				});
				tinyMCE.editors['productInfo_productDesc_modify'].setContent(productInfo.productDesc);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#productInfoModifyButton").click(function(){ 
		if ($("#productInfoModifyForm").form("validate")) {
			$("#productInfoModifyForm").form({
			    url:"ProductInfo/update/" + $("#productInfo_productNo_modify").val(),
			    onSubmit: function(){
					if($("#productInfoEditForm").form("validate"))  {
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
			$("#productInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
