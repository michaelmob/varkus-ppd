google.load("visualization", "1", { packages: ["geochart"] });

var colors = ["#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "F44336"];

var drawMapChart = function(data) {
	var table = new google.visualization.DataTable();
	table.addColumn("string", "Country");
	table.addColumn("number", "Conversions");
	table.addColumn("number", "Earnings");
	table.addRows(data);

	// Format second column
	var formatter = new google.visualization.NumberFormat({prefix: "$"});
	formatter.format(table, 2);

	var doDrawing = function() {
		var geoChart = new google.visualization.GeoChart($(".map.chart.container")[0]);

		google.visualization.events.addListener(geoChart, "ready", function() {
			$(".map.segment").removeClass("loading");
		});

		geoChart.draw(
			// Table Data
			table,

			// Options
			{
				width: "100%",
				height: "100%",
				dataMode: "regions",
				legend: { position: "none" },
				backgroundColor: "#FFF",
				colorAxis: { colors: colors },
				datalessRegionColor: "#EEE"
			}
		);
	};

	doDrawing();

	var resizeTimer;
	$(window).resize(function() {
		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(doDrawing(), 100);
	});

};

google.setOnLoadCallback(function() {
	$(".map.chart.container").api({
		url: window.location.href.split('?')[0] + "chart/map.json",
		on: "now",

		onSuccess: function(response) {
			drawMapChart(response.data);
		}
	});
});
