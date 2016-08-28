$(".ui.create.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	inline : true,
	fields: {
		category: {
			identifier : "category",
			rules: [{
				type   : "empty",
				prompt : "Please choose a category"
			}]
		},

		priority: {
			identifier : "priority",
			rules: [{
				type   : "empty",
				prompt : "Please choose a priority"
			}]
		},

		subject: {
			identifier : "subject",
			rules: [{
				type   : "empty",
				prompt : "Please enter your subject"
			}]
		},

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