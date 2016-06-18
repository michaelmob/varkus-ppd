var clickSound = null;
var conversionSound = null;
var bigConversionSound = null;

function createAudio(optionName) {
	var opt = Options.get(optionName);
	if(!opt || opt == "disabled") return;
	return opt ? new Audio("/static/sounds/" + opt + ".mp3") : null;
}

$(function() {
	/* Options */
	Options.load(function() {
		clickSound = createAudio("click-sound");
		conversionSound = createAudio("conversion-sound");
		bigConversionSound = createAudio("big-conversion-sound");
	});

	/* Elements */
	$(".ui.modal.options")
		.modal({
			onApprove: function() { Options.save(); return true; },
			onDeny: function() { Options.load(); return true; }
		})
		.modal("attach events", ".options.item", "show");

	$(".play.button").click(function() {
		var sound = $(this).siblings(".option").dropdown("get value");
		if(sound != "disabled")
			new Audio("/static/sounds/" + sound + ".mp3").play();
	});

	/* Websockets */
	var socket = new Socket(wsUrl);

	socket.onMessage = function(result) {
		if(!result.success)
			return;

		switch(result.type) {
			case "CONVERSION":
				// Play Sound
				if(result.data.payout < 10) {
					if(Options.get("conversion-sound"))
						conversionSound.play();
				} else {
					if(Options.get("big-conversion-sound"))
						bigConversionSound.play();
				}

				// Update Content
				setEarnings(result.data.user);
				return;

			case "TOKEN":
				// Play Sound
				if(Options.get("click-sound"))
					clickSound.play();

				// Update Content
				$.each($(".user.clicks"), function() {
					$(this).text(parseInt($(this).text()) + 1);

					if(document.hasFocus())
						$(this).transition("pulse");
				});
				return;

			case "NOTIFICATION":
				$(".notification.label").removeClass("hidden");
				$(".notifications.popup").load("/dashboard/notifications/ .ui.feed");
				return;
			
			default:
				return null;
		}
	};

	/* Page Values */
	var setPageData = function(selectorPrefix, data) {
		$.each(data, function(key, value) {
			var el = $(selectorPrefix + "." + key);

			if(el.text() == value)
				return;

			el.text(value);
			
			if(document.hasFocus())
				el.transition("pulse");
		});
	};

	var setEarnings = function(data) {
		setPageData(".user.clicks", data.clicks);
		setPageData(".user.conversions", data.conversions);
		setPageData(".user.earnings", data.earnings);
		setPageData(".user.epc", data.epc);

		$(".line.chart.container").api("query");
		$(".map.chart.container").api("query");
	};


	/* Notifications */
	$(".notifications.item").api({
		action: "read notifications",
		beforeSend: function(settings) {
			if($(".notification.label").hasClass("hidden"))
				return false;
		},
		onSuccess: function(response) {
			$(".notification.label").addClass("hidden");
			$(".special-notification.label").addClass("hidden");
		}
	});

});