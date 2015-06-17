$(".ui.modal.personal")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.personal.button", "show");

$(".ui.modal.account")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.account.button", "show");


$("form.personal").form({
	first_name: {
		identifier : "first_name",
		rules: [
			{
				type   : "empty",
				prompt : "Please specify your first name."
			}
		]
	},
	last_name: {
		identifier : "last_name",
		rules: [
			{
				type   : "empty",
				prompt : "Please specify your last name."
			}
		]
	},
	country: {
		identifier : "country",
		rules: [
			{
				type   : "empty",
				prompt : "Please choose your country."
			}
		]
	},
}, {
	inline : true,
	on : "blur"
});


$("form.account").form({
	email: {
		identifier : "email",
		rules: [
			{
				type   : "email",
				prompt : "Please enter your e-mail address."
			}
		]
	},
}, {
	inline : true,
	on : "blur"
});