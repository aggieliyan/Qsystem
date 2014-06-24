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
function change_p(id){
        $('#changeid').val(id);
        $('#myModal').modal('show');
      }
function delay_p(id,time){
        $('#delayid').val(id);
        $('#protime').val(time);
        $('#myModal1').modal('show');
      }


