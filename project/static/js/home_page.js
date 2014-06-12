$(document).ready(function(){
     $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-left",
        language:"zh-CN",
        minView:2
      });
	//点设计变更
    
    $(".change").on('click',function(){
    	$("#myModal").modal("show");
    });

});


