$(".ui.form").form({
	inline: true,

	fields: {
		name: {
			identifier : "name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your name."
			}]
		},

		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter your e-mail address."
			}]
		},

		complaint: {
			identifier : "complaint",
			rules: [{
				type   : "empty",
				prompt : "Please select a complaint type."
			}, {
				type   : "not[None]",
				prompt : "Please select a complaint type."
			}]
		},

		message: {
			identifier : "message",
			rules: [{
				type   : "length[20]",
				prompt : "Please enter atleast 20 characters of Content Links, Reasons and Evidence."
			}]
		}
	}
});