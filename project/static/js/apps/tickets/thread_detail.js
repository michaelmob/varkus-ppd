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

		if(response.data.status == "OPEN") {
			lbl.removeClass("red").addClass("green").text("Open");
		}

		else if(response.data.status == "CLOSED") {
			lbl.removeClass("green").addClass("red").text("Closed");
		}
    }
});


$(".delete").api({
	action: "post delete",
	method: "POST",
	beforeSend: function(settings) {
		if (!window.confirm("Are you sure you want to delete this post?"))
			return false;

		settings.urlData["id"] = tid;
		settings.data["csrfmiddlewaretoken"] = $("input[name='csrfmiddlewaretoken']").val();
		settings.data["pid"] = $(this).data("pid");
		return settings;
	},
	onSuccess: function(response) {
		if(response.data.status != "DELETED")
			return;
		$(this).parents(".comment").remove();

		if($(".comment").length < 1)
			document.location.href = "/tickets/";
	}
});


$("#id_file").change(function() {
	$("label[for='id_file'] span").text($(this).val());
});