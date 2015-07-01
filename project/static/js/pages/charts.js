google.load("visualization", "1", {packages:["geochart", "corechart"]});

var colors = [
	"#444", "#555", "#666", "#777"
];

var draw_map_chart = function(container, rows) {
	var data = new google.visualization.DataTable();
	data.addColumn("string", "Country");
	data.addColumn("number", "Earnings");
	data.addColumn("number", "Leads");
	data.addRows(rows);

	// Format second column
	var formatter = new google.visualization.NumberFormat({prefix: "$"});
	formatter.format(data, 1);

	new google.visualization.GeoChart(container[0]).draw
	(
		// Data
		data,

		// Options
		{
			//keepAspectRatio: false,
			width: "100%",
			height: "100%",
			dataMode: "regions",
			legend: {position: "none"},
			backgroundColor: "#FFF",
			colorAxis: {colors: colors},
			datalessRegionColor: "#efefef"
		}
	);
	$(".map.dimmer").removeClass("active");
};

var draw_line_chart_ex = function(container, rows, data) {
	new google.visualization.AreaChart(container[0]).draw
	(
		// Data
		data,

		// Options
		{
			pointSize: 5,
			chartArea: {
				left: 45,
				top: 35,
				width: container.width() - 70,
				height: container.parent().height() - 60
			},
			vAxis: {viewWindowMode: "explicit", viewWindow: {min: 0}},
			legend: {position: "none"},
			colors: colors
		}
	);
	$(".line.dimmer").removeClass("active");
};

var draw_line_chart = function(container, rows) {
	// Create Columns
	var data = new google.visualization.DataTable();
	data.addColumn("string", "Hour");
	data.addColumn("number", "Earnings");
	data.addColumn("number", "Leads");
	data.addRows(rows);

	// Format second column
	var formatter = new google.visualization.NumberFormat({prefix: "$"});
	formatter.format(data, 1);

	draw_line_chart_ex(container, rows, data);
};

var draw_line_chart_leads = function(container, rows) {
	// Create Columns
	var data = new google.visualization.DataTable();
	data.addColumn("string", "Hour");
	data.addColumn("number", "Leads");
	data.addRows(rows);

	draw_line_chart_ex(container, rows, data);
};