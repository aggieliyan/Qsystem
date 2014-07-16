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
      document.getElementById("mtab1").style.display = "none";
      document.getElementById("mtab2").style.display = "block";
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
      var stut = $(".basecolor").eq(i).children().eq(9).text();
      var d=new Date(Date.parse(time.replace(/-/g, "/")));
      var d=new Date(d.getTime() + 1*24*60*60*1000);
      var curDate=new Date();
      //var curDate1=curDate.toLocaleDateString(); 
      if(stut !='暂停' && stut != '已上线'){
        if(d){
          if(d < curDate){
            $(".basecolor").eq(i).css("background-color","#ff9933"); }
      }      
    };
    };


   //已完结项目中，翻页后，默认显示当前tab
    var tabcookievalue = $.cookie("mytab");
    //alert("tabcookievalue="+tabcookievalue);
    $("#myTab1 li").click(function () {
      $.cookie("mytab", $(this).index());
    });
    if (tabcookievalue == 1) {
      $("#myTab1").children().eq(0).removeClass("active");
      document.getElementById("mtab1").style.display = "none";
      $("#myTab1").children().eq(1).addClass("active");      
      document.getElementById("mtab2").style.display = "block";
      $("#mypage").show();
      $("#inpro").click(function () {
        $.cookie("mytab", " ");
        document.getElementById("mtab2").style.display = "none";
        document.getElementById("mtab1").style.display = "block";
    }); }
           
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

$(function(){
   //正在进行中给title赋值
   var cell=parseInt($(".procolor tr").length);
   for(var i=0; i<cell;i++){
    var user = $.trim($(".basecolor").eq(i).children().eq(5).text());
        user =user.replace(/\s+/g,' ');
    var project = $.trim($(".basecolor").eq(i).children().eq(1).text());
    $(".basecolor").eq(i).children().eq(1).attr("title",project);
    $(".basecolor").eq(i).children().eq(5).attr("title",user);
   } 
});

$(function(){
   //完结项目给title赋值
   var cell=parseInt($(".procolor1 tr").length);
   for(var i=0; i<cell;i++){
    var user = $.trim($(".basecolor1").eq(i).children().eq(5).text());
        user =user.replace(/\s+/g,' ');
    var project = $.trim($(".basecolor1").eq(i).children().eq(1).text());
    $(".basecolor1").eq(i).children().eq(1).attr("title",project);
    $(".basecolor1").eq(i).children().eq(5).attr("title",user);
   } 
});

(function(){
                //导航选中
                var url = location.pathname, navg = $('.top_memu li a');
                if(url == '/personal_homepage/?page=/'){
                    navg.eq(0).addClass('selected');
                }else if(!url.indexOf('/projectlist/')||!url.indexOf('/newproject/')||!url.indexOf('/detail/')||!url.indexOf('/editproject/')||!url.indexOf('/notice/')){
                    navg.eq(1).addClass('selected');
                }else if(!url.indexOf('/show_user/')||!url.indexOf('/sourcemanage/')||!url.indexOf('/show_source/')||!url.indexOf('/show_user2/')){
                    navg.eq(2).addClass('selected');
                }
            })()