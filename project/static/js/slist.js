$(document).ready(function(){

	$(".flip").click(function(){
		$(this).toggleClass("drapdown");
		var panel = $(this).parent().parent().next(".panel");
        content="这是一个内容很好<br/>这是一个内容很好<br/>这是一个内容很好<br/>这是一个内容很好<br/>"
		if(panel.length == 0){
			$(this).parent().parent().after("<tr class='row panel'><td><span>"+content+"<span></td></tr>");
		}else{
			panel.toggle();
		}

	});


});