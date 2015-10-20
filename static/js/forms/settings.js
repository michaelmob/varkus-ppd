$(".ui.modal.personal")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.personal.button", "show");

$(".ui.modal.account")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.account.button", "show");


$("form.personal").form({
	inline : true,
	fields: {
		first_name: {
			identifier : "first_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your first name"
			}]
		},
		last_name: {
			identifier : "last_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your last name"
			}]
		},
		country: {
			identifier : "country",
			rules: [{
				type   : "empty",
				prompt : "Please select your country"
			}]
		},
	});


$("form.account").form({
	inline : true,
	fields: {
		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter your e-mail address"
			}]
		},
	}
});