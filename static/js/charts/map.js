google.load("visualization", "1", { packages:["geochart"] });

var colors = [
	"#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "F44336"
];

var drawMapChart = function(container, data) {
	var table = new google.visualization.DataTable();
	table.addColumn("string", "Country");
	table.addColumn("number", "Earnings");
	table.addColumn("number", "Leads");
	table.addRows(data);

	// Format second column
	var formatter = new google.visualization.NumberFormat({prefix: "$"});
	formatter.format(table, 1);

	var doDrawing = function() {
		new google.visualization.GeoChart($(container)[0]).draw
		(
			// Table Data
			table,

			// Options
			{
				width: "100%",
				height: "100%",
				dataMode: "regions",
				legend: {position: "none"},
				backgroundColor: "#FFF",
				colorAxis: {colors: colors},
				datalessRegionColor: "#efefef"
			}
		);
	};

	doDrawing();

	var resizeTimer;
	$(window).resize(function() {
		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(doDrawing(), 100);
	});

	$(".map.dimmer").removeClass("active");
};

var loadMapChart = function() {
	$.ajax({
		url: dataUrl,
		type: "GET",
		dataType: "json",
		success: function(response) {
			drawMapChart(".map.chart.container", response.data);
		}
	});
};

google.setOnLoadCallback(loadMapChart);
