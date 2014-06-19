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
	document.form.action="/judge/";
	document.form.submit();
	});

});