$(document).ready(function(){

	$(".row a").click(function(){
		$(this).append("<tr class='row canremove'><td>哎呀呀 我这这里是展开的内容啊</td></tr>");
	});
}