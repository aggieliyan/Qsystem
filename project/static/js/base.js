$(document).ready(function(){
  	var today = new Date();
    var weekday=new Array(7)
    weekday[0]="Sat-Sun"
    weekday[1]="Mon"
    weekday[2]="Tue"
    weekday[3]="Wed"
    weekday[4]="Thu"
    weekday[5]="Fri"
    weekday[6]="Sat-Sun"                                    
    $("#logo").addClass(weekday[today.getDay()]);

	var url = "/user_info";
	$.get(url, function(data){
		var result = eval("\("+data+"\)");
		var name = result.realname;
		var pro_num = result.pro_num;
		var message_num = result.message_num;
		
		$(".mesage_right").text("("+pro_num+")");
		$("#message-num").text(message_num);
		
	    $(".top_bar a").eq(0).text(name);
	    if(name == "GUEST"){
	    	var bar = $(".top_bar a").eq(1)
	    	bar.text("登录");
	    	bar.attr("href","/login");

	    }
	});

	$(".judge").click(function()
	{
	document.form1.action="/judge/";
	document.form1.submit();
	});
});
(function(){
    //导航选中
    var url = location.pathname, navg = $('.top_memu li a');
    if(url == '/personal_homepage/'||url=='/historymessage/'||url=='/delay/'||url=='/myscore/'){
        navg.eq(0).addClass('selected');
    }else if(!url.indexOf('/projectlist/')||!url.indexOf('/newproject/')||!url.indexOf('/detail/')||!url.indexOf('/editproject/')||!url.indexOf('/notice/')){
        navg.eq(1).addClass('selected');
    }else if(!url.indexOf('/sdetail/')||!url.indexOf('/slist/')){
        navg.eq(2).addClass('selected');
    }else if(!url.indexOf('/scorelist/')||!url.indexOf('/viewscore/')){
		navg.eq(3).addClass('selected');
	}
})()