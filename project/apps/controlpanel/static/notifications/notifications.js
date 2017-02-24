$(function() {
	$(".notifications").popup({
		on: "click",
		position: "bottom right",
		onVisible: function() {
			var label_showing = $(".notifications.label").hasClass("hidden");
			var empty_content = $(".notifications.popup .content").text().length == 0;

			if(!(!label_showing || empty_content))
				return;

			var url = "/notifications/list/ #content";
			$(".notifications.dimmer").addClass("active");
			$(".notifications.popup .content").load(url, function() {
				$(".notifications.popup p").remove();
				$(".notifications.label").addClass("hidden");
				$(".notifications.dimmer").removeClass("active");
			});

			return true;
		}
	});
});