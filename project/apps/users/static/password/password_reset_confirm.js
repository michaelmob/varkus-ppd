$(".ui.form").form({
	inline : true,
	fields: {
		new_password1: {
			identifier : "new_password1",
			rules: [{
				type   : "empty",
				prompt : "Please enter your desired password"
			}]
		},

		new_password2: {
			identifier : "new_password2",
			rules: [{
				type   : "match[new_password1]",
				prompt : "Your new passwords do not match"
			}]
		}
	}
});