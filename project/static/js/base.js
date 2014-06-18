$(document).ready(function(){

	var url = "/showuser";
	$.get(url, function(data){
		var user = eval("\("+data+"\)");
		var name = user.realname;
	    $(".top_bar a").eq(0).text(name);
	});

});