$(document).ready(function(){
	var url = "/user_info";
	$.get(url, function(data){
		var result = eval("\("+data+"\)");
		var name = result.realname;		
	    $(".top_bar a").eq(0).text(name);
	    if(name == "GUEST"){
	    	var bar = $(".top_bar a").eq(1)
	    	bar.text("登录");
	    	bar.attr("href","/case/login");
	    }
	});
});
 (function(){
                //导航选中
                var url = location.pathname, navg = $('.top_memu li a');
                if(url == '/personal_homepage/'||url=='/historymessage/'||url=='/delay/'){
                    navg.eq(0).addClass('selected');
                }else if(!url.indexOf('/projectlist/')||!url.indexOf('/newproject/')||!url.indexOf('/detail/')||!url.indexOf('/editproject/')||!url.indexOf('/notice/')||!url.indexOf('/sdetail/')||!url.indexOf('/slist/')){
                    navg.eq(1).addClass('selected');
                }else if(!url.indexOf('/show_user/')||!url.indexOf('/sourcemanage/')||!url.indexOf('/show_source/')||!url.indexOf('/show_user2/')){
                    navg.eq(2).addClass('selected');
                }
            })()