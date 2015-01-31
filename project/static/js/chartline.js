function show_graph(pid){
	//var randomScalingFactor = function(){ return Math.round(Math.random()*100);};
	var url = "/getsdata/" + pid;
	$.get(url, function(data, status){
		var json = eval ("(" + data + ")");
		var i = 0;
		for (var key in json)		
			{
			
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
			
			var ctx = document.getElementsByName("canvas")[i].getContext("2d");
			window.myLine = new Chart(ctx).Line(lineChartData, {
				responsive: true
			});
			i = i+1;
			} //endfor
		});
	};