$("form").form({
	subject: {
		identifier : "subject",
		rules: [
			{
				type   : "empty",
				prompt : "Please enter your name."
			}
		]
	},

	priority: {
		identifier : "priority",
		rules: [
			{
				type   : "empty",
				prompt : "Please choose a priority."
			}
		]
	},

	type: {
		identifier : "type",
		rules: [
			{
				type   : "empty",
				prompt : "Please choose a type."
			}
		]
	},

	message: {
		identifier : "message",
		rules: [
			{
				type   : "length[20]",
				prompt : "Please enter atleast 20 characters in the message field."
			}
		]
	}
});