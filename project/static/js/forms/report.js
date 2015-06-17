$("form").form({
	name: {
		identifier : "name",
		rules: [
			{
				type   : "empty",
				prompt : "Please enter your name."
			}
		]
	},

	email: {
		identifier : "email",
		rules: [
			{
				type   : "email",
				prompt : "Please enter a valid e-mail address."
			}
		]
	},

	complaint: {
		identifier : "complaint",
		rules: [
			{
				type   : "empty",
				prompt : "Please choose a complaint type."
			}
		]
	},

	text: {
		identifier : "text",
		rules: [
			{
				type   : "length[20]",
				prompt : "Please enter atleast 20 characters of Content Links, Reasons and Evidence."
			}
		]
	}
});

$(".upload-images").click(function() { $(".images").toggle(); });