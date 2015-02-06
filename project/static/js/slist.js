$(document).ready(function(){
	var id=0;
	$(".flip").click(function(){
		if ($(".panel").length != id){
			id++;
		}
		$(this).toggleClass("drapdown");
		pid = $(this).attr("value");
		var panel = $(this).parent().parent().next(".panel");
		if(panel.length == 0){
		    $(this).parent().parent().after("<tr class='row panel'><td id='"+id+"'></td></tr>");
			var url = "/sflip/" + pid;
			$.get(url, function(data, status){
				var datalist = eval ("(" + data + ")");
				var num = datalist.length;
				for(var i=0;i<num;i++){
					$("#"+id).append("<div><p>"+datalist[i].item+":"+"</p><p>"+datalist[i].num+"</p></div><div style='width:60%;'><canvas id='canvas"+id+datalist[i].sql+"' height='2' width='3'></canvas></div>");
                    if(i<num-1){
					    $("#"+id).append("<div><p style=\"color:#7B7B7B\">------------------------------------------------------------------------</p></div>");
                    }
				}				
			});				
			setTimeout(500);	
			show_graph(pid,id);		
		}
		else{
			panel.toggle();
		}
	});
});