$(document).ready(function(){

	var url = "/showuser";
	$.get(url, function(data){
		var user = eval("\("+data+"\)");
		var name = user.realname;
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
	      
    $(function(){
        var url1 = "/show_pronum";
        $.get(url1,function(data){
        $(".mesage_right").text("("+data+")");
        });
     });       
    $(function(){
        var url2 = "/show_messagenum";
        $.get(url2,function(data){
        $("#message-num").text(data);
        });
           
    });

});
 (function(){
                //导航选中
                var url = location.pathname, navg = $('.top_memu li a');
                if(url == '/personal_homepage/'||url=='/historymessage/'||url=='/delay/'){
                    navg.eq(0).addClass('selected');
                }else if(!url.indexOf('/projectlist/')||!url.indexOf('/newproject/')||!url.indexOf('/detail/')||!url.indexOf('/editproject/')||!url.indexOf('/notice/')){
                    navg.eq(1).addClass('selected');
                }else if(!url.indexOf('/show_user/')||!url.indexOf('/sourcemanage/')||!url.indexOf('/show_source/')||!url.indexOf('/show_user2/')){
                    navg.eq(2).addClass('selected');
                }
            })()

           