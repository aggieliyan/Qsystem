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
    
    $("#inpro").click(function(){
      console.log("hahhtjh");
      $("#mypage").hide();
    });

    $(".chomdelay").click(function(){
       timepro=$(this).parent().parent().children().eq(7).text();
       if (!timepro)
       {
        alert("计划上线时间为空不可申请延期");
        }
      }); 
 
     $("#changepro").click(function(){
       $.trim($("#as").val())
     });    

    //超过上线日期时显示橙色
    var cellIndex=parseInt($(".procolor tr").length);
    for(var i=0; i<cellIndex;i++) {
      var time =document.getElementsByName("datetime")[i].value;
      //print time;
      var d=new Date(Date.parse(time.replace(/-/g, "/")));
      var curDate=new Date();
      if(d){
        if(d<curDate){
        $(".basecolor").eq(i).css("background-color","#ff9933"); }
      }      
    };
});

(function(){
  //通过路径获取当前页
  var url = location.pathname, navg = $('.top_memu li a');
  if(url == '/personal_homepage/'){
    $("#mypage").hide();
    }
  })()
            
function AutoClick()
{ 
    
    var myLink = document.getElementById("finshedpro");
    myLink.click();

}

function change_p(id){
        $('#changeid').val(id);
        $('#myModal').modal('show');
      }
      function delay_p(id,time){
        $('#delayid').val(id);
        $('#protime').val(time);
        $('#myModal1').modal('show');
      }
      function chk(){
        var chcontent = document.test.cont.value;
        var chdpath = document.test.dpath.value;
        if(!chcontent||!chdpath){
          alert('变更内容或设计图路径不能为空');
        }
        else{
          document.test.submit();
        } 
      }
      function chkdelay(){
        var delaytime = document.test1.delay_date.value;
        var delayreason = document.test1.delay_reason.value;
        if(!delaytime||!delayreason){
          alert('延期日期或者延期理由不能为空');
        }
        else{
          document.test1.submit();
        } 
      }

$(function(){
   var cellIndex=parseInt($(".prorealter tr").length-1);
   $(".prorealter tr td").each(function(){
        if(this.cellIndex = cellIndex){
            $(this).attr("title",$(this).text());
            //alert($(this).parent().get(0).rowIndex);输出所在行
          }
   });
});


