$(".ui.form").form({
	inline : true,
	fields: {
		username: {
			identifier: "username",
			rules: [{
				type: "empty",
				prompt: "Please enter your username or e-mail"
			}]
		},
		password: {
			identifier: "password",
			rules: [{
				type: "empty",
				prompt: "Please enter your password"
			}]
		}
	}
});