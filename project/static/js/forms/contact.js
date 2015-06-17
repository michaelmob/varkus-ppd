$("form").form({
	name: {
		identifier : "name",
		rules: [
			{
				type   : "empty",
				prompt : "Please enter your name."
			}
		]
	},

	email: {
		identifier : "email",
		rules: [
			{
				type   : "email",
				prompt : "Please enter a valid e-mail address."
			}
		]
	},

	subject: {
		identifier : "subject",
		rules: [
			{
				type   : "length[10]",
				prompt : "Your subject must be longer than 10 characters."
			}
		]
	},

	message: {
		identifier : "message",
		rules: [
			{
				type   : "length[20]",
				prompt : "Your message must be longer than 20 characters."
			}
		]
	}
});