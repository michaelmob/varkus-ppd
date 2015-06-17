$("form").form({
	first_name: {
		identifier  : "first_name",
		rules: [
			{
				type	: "empty",
				prompt	: "Please enter your first name."
			}
		]
	},
	last_name: {
		identifier  : "last_name",
		rules: [
			{
				type	: "empty",
				prompt	: "Please enter your last name."
			}
		]
	},
	username: {
		identifier : "username",
		rules: [
			{
				type	: "empty",
				prompt	: "Please enter a username."
			}
		]
	},
	email: {
		identifier : "email",
		rules: [
			{
				type	: "email",
				prompt	: "Please enter a valid e-mail address."
			}
		]
	},
	password: {
		identifier : "password",
		rules: [
			{
				type	: "empty",
				prompt	: "Please enter a password."
			},
			{
				type	: "length[6]",
				prompt	: "Your password must be at least 6 characters."
			}
		]
	},
	confirm: {
		identifier : "confirm",
		rules: [
			{
				type	: "match[password]",
				prompt	: "Your passwords must match."
			}
		]
	}
});

// Populate days dropbox
for(var i = 1; i < 32; i++) {
	$(".date-day").append("<div class=\"item\">" + i + "</div>");
}


// Populate months dropbox
var months = [
	"January", "February", "March", "April", "May", "June",
	"July", "August", "September", "October", "November", "December"
];

for(var i = 0; i < months.length; i++) {
	$(".date-month").append("<div class=\"item\" data-value=\"" + (i+1) + "\">" + months[i] + "</div>");
}


// Populate years dropbox
var year = new Date().getFullYear();

for(var i = year; i > year - 100; i--) {
	$(".date-year").append("<div class=\"item\">" + i + "</div>");
}