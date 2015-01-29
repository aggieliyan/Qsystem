var randomScalingFactor = function(){ return Math.round(Math.random()*100);};
var lineChartData = {
		labels : ["1月","2月","3月","4月","5月","6月","7月"],
		datasets : [
			{
				label: "My dataset",
				fillColor : "rgba(220,220,220,0)",
				strokeColor : "rgba(255,153,51,1)",
				pointColor : "#fff",
				pointStrokeColor : "rgba(255,153,51,1)",
				pointHighlightFill : "rgba(220,220,220,1)",
				pointHighlightStroke : "rgba(255,153,51,1)",
				data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
			},

		]

};

window.onload = function(){
	var ctx = document.getElementById("canvas").getContext("2d");
	window.myLine = new Chart(ctx).Line(lineChartData, {
		responsive: true
	});
};