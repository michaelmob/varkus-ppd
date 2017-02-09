var forms = {
	paypal: {
		paypal_email: {
			identifier : "paypal-email",
			rules: [{
				type   : "email",
				prompt : "Please enter your Paypal Email"
			}]
		},
	},

	check: {
		check_pay_to: {
			identifier : "check-pay_to",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full name"
			}]
		},
		check_address: {
			identifier : "check-address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your full address"
			}]
		},
	},

	wire: {
		wire_beneficiary_name: {
			identifier : "wire-beneficiary_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter the beneficiary's name"
			}]
		},
		wire_account_number: {
			identifier : "wire-account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number"
			}]
		},
		wire_bank_name: {
			identifier : "wire-bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name"
			}]
		},
		wire_routing_aba_swift: {
			identifier : "wire-routing_aba_swift",
			rules: [{
				type   : "empty",
				prompt : "Please enter the Routing Number / ABA / Swift"
			}]
		},
		wire_bank_address: {
			identifier : "wire-bank_address",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's address"
			}]
		},
	},

	direct: {
		direct_account_holder: {
			identifier : "direct-account_holder",
			rules: [{
				type   : "empty",
				prompt : "Please enter the account holder's name"
			}]
		},
		direct_account_number: {
			identifier : "direct-account_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your account number"
			}]
		},
		direct_routing_number: {
			identifier : "direct-routing_number",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's routing number"
			}]
		},
		direct_bank_name: {
			identifier : "direct-bank_name",
			rules: [{
				type   : "empty",
				prompt : "Please enter your bank's name"
			}]
		},
	},
};


$(".ui.tabular.menu .item").tab({
	onLoad: function(tab_name) {
		$("form[data-tab=" + tab_name + "]").form({
			inline: true, fields: forms[tab_name]
		});
	}
}).tab("change tab", active_tab);


$(".submit.button").click(function() {
	$("form[data-tab=" + $(".active.tab").attr("data-tab") + "]").form("submit");
});