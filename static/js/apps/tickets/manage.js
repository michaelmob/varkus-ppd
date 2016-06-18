$("form").form({
	inline : true,
	fields: {
		message: {
			identifier : "message",
			rules: [{
				type   : "empty",
				prompt : "Please enter your message"
			}, {
				type   : "maxLength[5000]",
				prompt : "A maximum of 5000 characters may be used"
			}]
		},
	}
});

$(".status.item").api({
	action: "ticket status",
	onSuccess: function(response) {
		var lbl = $(".label.status");

		if(response.data.status == "OPEN")
			lbl.removeClass("red").addClass("green").text("Open");

		else if(response.data.status == "CLOSED")
			lbl.removeClass("green").addClass("red").text("Closed");
    }
});