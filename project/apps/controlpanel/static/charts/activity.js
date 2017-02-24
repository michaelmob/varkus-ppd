var flotData = null;
var desktopScreen = $(window).width() > 1300;

var amPMTickFormatter = function (n, s) {
	s = n > 12 ? "p" : "a";
	s = (((n + 11) % 12) + 1) + s;
	s = n != hour ? s : "<strong>" + s + "</strong>";
	return s;
};

var tfTickFormatter = function (n, s) {
	return n != hour ? n : "<strong>" + n + "</strong>";
};

var flotOptions = {
	points: {
		radius: 3.5,
		symbol: "circle"
	},
	colors: ["#f44336", "#2185d0", "#1cb842"],
	shadowSize: 0,
	yaxis: {
		minTickSize: 1,
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

			return label + ": <strong>" + yval + "</strong>";
		},
	}
};

$(".activity.chart.container").api({
	stateContext: ".activity.segment",
	url: window.location.href.split('?')[0] + "activity.json",
	on: "now",

	onSuccess: function(response) {
		var data = response.data;
		var new_data = [
			{label: "Clicks", data: []},
			{label: "Conversions", data: []},
			{label: "Earnings", data: []},
		];

		if(!desktopScreen)
			for (var i = 0; i < data.length; i++)
				if(data[i].data)
					data[i].data.splice(hour < 1 ? 12 : 0, 12);

		for (var i = 0; i < Object.keys(data).length; i++)
			for (var j = 0; j < 3; j++)
				new_data[j]["data"].push([i, data[i][j]]);

		$.plot(".activity.chart.container", new_data, flotOptions);
	}
});
