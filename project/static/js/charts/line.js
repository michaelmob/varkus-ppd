flotData = null;

var amPMTickFormatter = function (n, s) {
	s = n > 12 ? "p" : "a";
	s = (((n + 11) % 12) + 1) + s;
	s = n != hour ? s : "[" + s + "]"
	return s;
};

var tfTickFormatter = function (n, s) {
	return n != hour ? n : "<strong>" + n + "</strong>";
};

var flotOptions = {
	points: {
		radius: 2,
		symbol: "circle"
	},
	colors: ["#f44336", "#2185d0", "#1cb842"],
	shadowSize: 0,
	yaxis: {
		tickSize: 1,
		min: 0,
	},
	xaxis: {
		tickFormatter: tfTickFormatter,
		tickSize: 1
	},
	grid: {
		color: "#aaa",
		borderWidth: 0,
		hoverable: true,
	},
	series: {
		lines: { show: true, },
		points: { show: true },
	},
	legend: {
		backgroundOpacity: 0,
		labelBoxBorderColor: null
	},
	tooltip: {
		show: true,
		cssClass: "plotTip",
		content: function(label, xval, yval) {
			if(label == "Earnings") {
				yval = "$" + parseFloat(yval).toFixed(2);
			}
			
			return label + ": " + yval;
		},
	}
};

var loadLineChart = function() {
	$.ajax({
		url: dataUrl,
		type: "GET",
		dataType: "json",
		success: function(response) {
			flotData = response;
			$(".line.chart.container").height(195);
			$.plot(".line.chart.container", response.data, flotOptions);
			$(".line.dimmer").removeClass("active");
		}
	});
};

loadLineChart();