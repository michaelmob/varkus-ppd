$(".ui.modal.edit").modal({
	observeChanges: true,
	onApprove: function() {
		return false;
	},
}).modal("attach events", ".edit.button", "show");

$(".ui.details.button").popup({
	on: "click",
	transition: "fade up"
});

$(".ui.tabular.menu .item").tab({
	onLoad: function() {
		$(".ui.modal.edit").modal("refresh");
	}
});

$(".ui.paypal.form").form({
	inline: true,
	fields: {
		paypal_email: {
			identifier : "paypal_email",
			rules: [{
				type   : "email",
				prompt : "Please enter your Paypal Email."
			}]
		},
	}
});

$(".ui.check.form").form({
	inline: true,
	fields: {
		check_pay_to: {
			identifier : "check_pay_to",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full name."
			}]
		},
		check_address: {
			identifier : "check_address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full address."
			}]
		},
	}
});

$(".ui.wire.form").form({
	inline: true,
	fields: {
		wire_beneficiary_name: {
			identifier : "wire_beneficiary_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter the beneficiary's name."
			}]
		},
		wire_account_number: {
			identifier : "wire_account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number."
			}]
		},
		wire_bank_name: {
			identifier : "wire_bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name."
			}]
		},
		wire_routing_aba_swift: {
			identifier : "wire_routing_aba_swift",
			rules: [{
				type   : "empty",
				prompt : "Please enter the Routing / ABA / Swift."
			}]
		},
		wire_bank_address: {
			identifier : "wire_bank_address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's address."
			}]
		},
	}
});

$(".ui.direct.form").form({
	inline: true,
	fields: {
		direct_account_holder: {
			identifier : "account_holder",
			rules: [{
				type   : "empty",
				prompt : "Please enter the account holder's name."
			}]
		},
		direct_account_number: {
			identifier : "direct_account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number."
			}]
		},
		direct_routing_number: {
			identifier : "direct_routing_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's routing number."
			}]
		},
		direct_bank_name: {
			identifier : "direct_bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name."
			}]
		},
	}
});