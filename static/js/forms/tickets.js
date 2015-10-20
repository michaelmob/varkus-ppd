$("form").form({
	inline : true,
	fields: {
		subject: {
			identifier : "subject",
			rules: [{
				type   : "empty",
				prompt : "Please enter your name"
			}]
		},

		priority: {
			identifier : "priority",
			rules: [{
				type   : "empty",
				prompt : "Please select a priority"
			}]
		},

		type: {
			identifier : "type",
			rules: [{
				type   : "empty",
				prompt : "Please select a type"
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