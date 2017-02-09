$(".priority.item").api({
	method: "POST",
	action: "offer priority",
	beforeSend: function(settings) {
		settings.data.value = $(this).attr("data-value");
		return settings;
	}
});


$(".boost.item").api({
	method: "POST",
	action: "offer boost",
	onSuccess: function(response) {
		$(".boost.message").removeClass("hidden");
		$(".boost.count").text(response.data.count.toString());

		if(document.hasFocus())
			$(".boost.count").transition("pulse");
	}
});


$(".reset.item").api({
	method: "POST",
	action: "offer reset",
	onSuccess: function(response) {
		$(".boost.message").addClass("hidden");
	}
});