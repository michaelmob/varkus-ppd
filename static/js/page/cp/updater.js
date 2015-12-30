$(function() {
	var ws4redis = WS4Redis({
		uri: uri + "cp?subscribe-user",
		heartbeat_msg: "--heartbeat--",
		receive_message: function(data) {
			data = $.parseJSON(data);

			if(!data.success) {
				return;
			}

			switch(data.type) {
				case "LEAD":
					playSound();
					return updateEarnings(data.data.user);

				case "TOKEN":
					return updateClicks(data.data.user);
				
				default:
					return null;
			}
		},
	});

	var playSound = function() {
		var file = localStorage.getItem("opt_notification-sound");
		
		if(file == "none") {
			return;
		}

		var audio = new Audio("/static/sounds/" + (file || "bell") + ".mp3");
		audio.play();
	};

	var updateChange = function(selector, value) {
		if($(selector).text() == value) {
			return;
		}

		$(selector).text(value).transition("pulse");
	};

	var updateEarnings = function(user) {
		var kv = {
			".user.clicks.today": user.clicks_today,
			".user.clicks.total": user.clicks,

			".user.leads.today": user.leads_today,
			".user.leads.total": user.leads,

			".user.earnings.today": user.today,
			".user.earnings.week": user.week,
			".user.earnings.month": user.month,
			".user.earnings.year": user.year,
			".user.earnings.total": user.total,
			".user.epc.today": user.clicks_today > 0 ? 
				(user.today / user.clicks_today).toFixed(2) : 0
		};

		$.each(kv, function(k, v) {
			updateChange(k, v);
		});

		$(".line.chart.container").api("query");
		$(".map.chart.container").api("query");
	};

	var updateClicks = function(user) {
		var kv = {
			".user.clicks.today": user.clicks_today,
			".user.clicks.total": user.clicks
		};

		$.each(kv, function(k, v) {
			updateChange(k, v);
		});
	};
});