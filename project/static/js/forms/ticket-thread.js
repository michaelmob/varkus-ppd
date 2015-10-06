$("form").form({
	inline : true,
	fields: {
		message: {
			identifier : "message",
			rules: [{
				type   : "length[5]",
				prompt : "Your message must be at least 5 characters"
			}]
		}
	}
});