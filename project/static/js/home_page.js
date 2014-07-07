$(document).ready(function(){
     $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-left",
        language:"zh-CN",
        minView:2 
      });
	
    $("#smalltable").click(function(){
      console.log("aaaaaaaa");
      $("#mybody").css("width","1100px");
      $("#x-table2").css("width","1100px");
    });

    $("#bigtable").click(function(){
      $("#mybody").css("width","1500px");
      $("#x-table2").css("width","1500px");
    });



    $("#finishedpro").click(function(){
      console.log("hahhtjh");
      $("#mypage").show();
    });
    $("#inpro").click(function(){
      console.log("hahhtjh");
      $("#mypage").hide();
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

(function(){
                //通过路径获取当前页
                var url = location.pathname, navg = $('.top_memu li a');
                if(url == '/personal_homepage/'){
                    $("#mypage").hide();
                }
            })()


