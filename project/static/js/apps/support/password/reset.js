$("form").form({
	inline : true,
	fields: {
		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter your e-mail address"
			}]
		}
	}
});