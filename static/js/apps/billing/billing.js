var fields = {
	paypal: {
		paypal_email: {
			identifier : "paypal-email",
			rules: [{
				type   : "email",
				prompt : "Please enter your Paypal Email."
			}]
		},
	},

	check: {
		check_pay_to: {
			identifier : "check-pay_to",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full name."
			}]
		},
		check_address: {
			identifier : "check-address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full address."
			}]
		},
	},

	wire: {
		wire_beneficiary_name: {
			identifier : "wire-beneficiary_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter the beneficiary's name."
			}]
		},
		wire_account_number: {
			identifier : "wire-account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number."
			}]
		},
		wire_bank_name: {
			identifier : "wire-bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name."
			}]
		},
		wire_routing_aba_swift: {
			identifier : "wire-routing_aba_swift",
			rules: [{
				type   : "empty",
				prompt : "Please enter the Routing / ABA / Swift."
			}]
		},
		wire_bank_address: {
			identifier : "wire-bank_address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's address."
			}]
		},
	},

	direct: {
		direct_account_holder: {
			identifier : "direct-account_holder",
			rules: [{
				type   : "empty",
				prompt : "Please enter the account holder's name."
			}]
		},
		direct_account_number: {
			identifier : "direct-account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number."
			}]
		},
		direct_routing_number: {
			identifier : "direct-routing_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's routing number."
			}]
		},
		direct_bank_name: {
			identifier : "direct-bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name."
			}]
		},
	},
};

$(".ui.modal.edit")
	.modal({ onApprove: function() { return false; }, })
	.modal("attach events", ".edit.button", "show");

$("form[data-tab=paypal]").form({ inline: true, fields: fields.paypal });
$("form[data-tab=check]").form({ inline: true, fields: fields.check});
$("form[data-tab=wire]").form({ inline: true, fields: fields.wire });
$("form[data-tab=direct]").form({ inline: true, fields: fields.direct });


$(".ui.tabular.menu .item")
	.tab({
		onLoad: function(tab) {
			_tab = tab;
			$(".ui.modal.edit").modal("refresh");
		}
	})
	.tab("change tab", active_tab);

$(".ui.modal.edit .submit.button").click(function() {
	$("form[data-tab=" + $(".active.tab").attr("data-tab") + "]")
		.form("submit");
});