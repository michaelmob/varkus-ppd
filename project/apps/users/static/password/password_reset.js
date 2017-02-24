$(".ui.form").form({
	inline : true,
	fields: {
		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter a valid e-mail address"
			}]
		}
	}
});