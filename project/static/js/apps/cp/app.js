var audio = null;


$(function() {

	/*
	* Settings
	*/
	Settings.load(function() {
		audio = new Audio().initiate();
	});


	/*
	* WebSockets
	*/
	var socket = new Socket(wsUrl);

	socket.onMessage = function(result) {
		if(!result.success)
			return;

		switch(result.type) {
			case "CONVERSION":
				// Play Sound
				audio.playConversion(result.data.payout > 10);

				// Update Content
				updateEarnings(result.data.user);
				return;

			case "TOKEN":
				// Play Sound
				audio.playClick();

				// Update Content
				$.each($(".user.clicks"), function() {
					$(this).text(parseInt($(this).text()) + 1);

					if(document.hasFocus())
						$(this).transition("pulse");
				});
				return;

			case "BROADCAST":
			case "NOTIFICATION":
				var value = parseInt($(".notifications.label").text()) || 0;
				$(".notifications.label").text((value+1).toString()).removeClass("hidden");
				return;
			
			default:
				return null;
		}
	};


	/*
	* Page Content Updating Helpers
	*/
	var updateElements = function(selectorPrefix, data) {
		$.each(data, function(key, value) {
			var el = $(selectorPrefix + "." + key);

			if(el.text() == value)
				return;

			el.text(value);
			
			if(document.hasFocus())
				el.transition("pulse");
		});
	};

	var updateEarnings = function(data) {
		updateElements(".user.clicks", data.clicks);
		updateElements(".user.conversions", data.conversions);
		updateElements(".user.earnings", data.earnings);
		updateElements(".user.epc", data.epc);

		$(".line.chart.container").api("query");
		$(".map.chart.container").api("query");
	};

});