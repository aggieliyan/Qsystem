$(document).ready(function(){
	var id=0;
	$(".sbox td").click(function(){
		if ($(".panel").length != id){
			id++;
		}
		var traicon = $(this).children('.flip');
		traicon.toggleClass("drapdown");
		pid = traicon.attr("value");
		var panel = traicon.parent().parent().next(".panel");
		if(panel.length == 0){
		    traicon.parent().parent().after("<tr class='row panel'><td id='"+id+"'></td></tr>");
			var url = "/sflip/" + pid;
			$.get(url, function(data, status){
				var datalist = eval ("(" + data + ")");
				var num = datalist.length;
				for(var i=0;i<num;i++){
					$("#"+id).append("<div><p>"+datalist[i].item+":"+"</p><p>"+datalist[i].num+"</p></div><div style='width:60%;'><canvas id='canvas"+id+datalist[i].sql+"' height='2' width='3'></canvas></div>");
                    if(i<num-1){
					    $("#"+id).append("<div><hr style=\"border:1px dotted #7B7B7B\" /></div>");
                    }
				}
				show_graph(pid,id);				
			});							
		}
		else{
			panel.toggle();
		}
	});
});