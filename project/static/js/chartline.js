function show_graph(pid,id){
	var url = "/getsdata/" + pid;
	$.get(url, function(data, status){
		var json = eval ("(" + data + ")");
		var i = 0;
		for (var key in json){
			var lineChartData = {
					labels : json[key].labels,
					datasets : [
						{
							label: "My dataset",
							fillColor : "rgba(220,220,220,0)",
							strokeColor : "rgba(255,153,51,1)",
							pointColor : "#fff",
							pointStrokeColor : "rgba(255,153,51,1)",
							pointHighlightFill : "rgba(220,220,220,1)",
							pointHighlightStroke : "rgba(255,153,51,1)",
							data : json[key].total
						},		
					]		
			}; //endData			
			var ctx = document.getElementById("canvas"+id+i).getContext("2d");
			// console.log(document.getElementById("canvas"+id+i));
			window.myLine = new Chart(ctx).Line(lineChartData, {
				responsive: true
			});
			i = i+1;
			} //endfor
		});
	};