$("form").form({
	message: {
		identifier : "message",
		rules: [
			{
				type   : "length[5]",
				prompt : "Please enter atleast 5 characters in the message field."
			}
		]
	}
});