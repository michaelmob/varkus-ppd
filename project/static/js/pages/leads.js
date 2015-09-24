$(function() {
	var settings, title, idleSeconds;
	var pollInterval, titleInterval;
	var leads = parseInt($("#leads").text());

	$("time").timeago();

	$(".two.item.menu .item").tab();

	var saveSettings = function() {
		settings = {
			"leads-sound": $("#setting-sound").dropdown("get value"),
			"leads-update": $("#setting-update").checkbox("is checked"),
			"leads-title": $("#setting-title").checkbox("is checked"),
		};

		for(var key in settings) {
			localStorage.setItem(key, settings[key]);
		}
	};

	var getSettingBoolean = function (key) {
		return localStorage.getItem(key) == "false" ? "uncheck" : "check";
	};

	var loadSettings = function() {
		$("#setting-sound").dropdown("set selected", localStorage.getItem("leads-sound") || "bell");
		$("#setting-update").checkbox(getSettingBoolean("leads-update"));
		$("#setting-title").checkbox(getSettingBoolean("leads-title"));
	};

	var playSound = function() {
		var sound = $("#setting-sound").dropdown("get value");

		if(sound.length > 1 && sound != "none") {
			new Audio("/static/sounds/" + sound + ".mp3").play();
		}
	};

	var updateTime = function() {
		$("time").each(function() {
			var p = $(this).parent().parent();
			if($(this).text().match("e ago$"))
				p.css("background-color", "lightgoldenrodyellow");
			else
				p.css("background-color", "initial");
		});
	};

	var reloadEarnings = function() {
		$(".earnings.content").load(location.href + " .earnings.content > *", function() {
			$(".two.item.menu .item").tab();
		});
	};

	var reloadLeads = function() {
		$(".leads.content").load(location.href + " .leads.content > *", function() {
			$("time").timeago();
			updateTime();
		});
	};

	var flashTitle = function() {
		clearInterval(titleInterval);

		titleInterval = setInterval(function() {
			title = document.title;

			if(!document.hidden) {
				document.title = title;
				clearInterval(titleInterval);
			}

			document.title = "New Lead | Varkus"

			setTimeout(function() {
				document.title = title;
			}, 1000);
		}, 3000);
	};

	var pollLeads = function() {
		if(idleSeconds > 900)
			return;

		if(!$("#setting-update").checkbox("is checked"))
			return;

		$.get("/dashboard/leads/poll", function(data) {
			try {
				newLeads = parseInt(data);
			} catch (e) {
				console.log(e);
				alert("Something went wrong while checking for new leads!");
				clearInterval(pollInterval);
				return;
			}

			if(newLeads > leads) {
				playSound();
				flashTitle();

				reloadEarnings();
				reloadLeads();

				leads = newLeads;
			}
		});
	};

	var pollIdle = function() {
		idleSeconds = document.hidden ? idleSeconds + 1 : 0;
	};

	var startPoll = function() {
		clearInterval(pollInterval);
		pollInterval = setInterval(pollLeads, 15 * 1000);
		titleInterval = setInterval(pollIdle, 1000);
	};

	$(".save.button").click(function() {
		saveSettings();

		var _this = $(this);
		var prev = _this.text();
		_this.addClass("loading");

		setTimeout(function() {
			_this.removeClass("loading");
			_this.text("Saved!");
		}, 250);

		setTimeout(function() {
			_this.text(prev);
		}, 1000);
	});

	$(".play.button").click(playSound);

	loadSettings();
	startPoll();

	reloadEarnings();
});