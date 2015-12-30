$("form").form({
	inline: true,
	fields: {
		first_name: {
			identifier: "name",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your name"
			}]
		},
		email: {
			identifier: "email",
			rules: [{
				type	: "email",
				prompt	: "Please enter your e-mail address"
			}]
		},
		username: {
			identifier: "username",
			rules: [{
				type	: "empty",
				prompt	: "Please enter a username"
			}]
		},
		password: {
			identifier: "password1",
			rules: [{
				type	: "empty",
				prompt	: "Please enter a password"
			}, {
				type	: "length[6]",
				prompt	: "Your password must be at least 6 characters"
			}]
		},
		confirm: {
			identifier: "password2",
			rules: [{
				type	: "match[password1]",
				prompt	: "Your passwords must match"
			}]
		},
		agree: {
			identifier: "agree",
			rules: [{
				type	: "checked",
				prompt	: "You must agree to the Terms and Conditions"
			}]
		}
	}
});
