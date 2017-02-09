$("#id_birthdate").parent().calendar({
	type: "date",
	startMode: "year",
	formatter: {
		date: function (date, settings) {
			var year = date.getFullYear();
			var month = ("0" + (date.getMonth() + 1)).slice(-2);
			var day = ("0" + (date.getDate())).slice(-2);
			return month + "/" + day + "/" + year;
		}
	}
});


$(".ui.form").form({
	inline: true,
	fields: {
		username: {
			identifier: "username",
			rules: [{
				type	: "empty",
				prompt	: "Please enter a username"
			}]
		},
		email: {
			identifier: "email",
			rules: [{
				type	: "email",
				prompt	: "Please enter your e-mail address"
			}]
		},
		password: {
			identifier: "password1",
			rules: [{
				type	: "empty",
				prompt	: "Please enter a password"
			}, {
				type	: "length[8]",
				prompt	: "Your password must be at least 8 characters long"
			}]
		},
		confirm: {
			identifier: "password2",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your password again"
			}, {
				type	: "match[password1]",
				prompt	: "Your passwords must match"
			}]
		},
		birthdate: {
			identifier: "birthdate",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your birthdate"
			}]
		},
		agree: {
			identifier: "agree",
			rules: [{
				type	: "checked",
				prompt	: "You must agree to the Terms of Service"
			}]
		}
	}
});