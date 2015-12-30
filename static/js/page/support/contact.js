$("form").form({
	inline : true,

	fields: {
		name: {
			identifier : "name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your name"
			}]
		},

		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter your e-mail address"
			}]
		},

		subject: {
			identifier : "subject",
			rules: [{
				type   : "length[10]",
				prompt : "Your subject must be at least 10 characters"
			}]
		},

		message: {
			identifier : "message",
			rules: [{
				type   : "length[20]",
				prompt : "Your message must be at least 20 characters"
			}]
		}
	}
});