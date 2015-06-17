$("form").form({
	email: {
		identifier : "email",
		rules: [
			{
				type   : "email",
				prompt : "Please enter a valid e-mail address."
			}
		]
	}
});