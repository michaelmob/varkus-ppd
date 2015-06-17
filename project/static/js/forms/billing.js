$(".ui.modal.edit.account")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.button", "show");


var set_invisible = function() {
	$("#paypal").hide();
	$("#check").hide();
	$("#wire").hide();
	$("#direct").hide();
}


var form_paypal = function() {
	$("form").form({
		paypal_email: {
			identifier : "paypal_email",
			rules: [
				{
					type   : "email",
					prompt : "Please enter your Paypal Email."
				}
			]
		},
	}, {
		inline : true,
		on : "blur"
	});
};


var form_check = function() {
	$("form").form({
		check_pay_to: {
			identifier : "check_pay_to",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your full name."
				}
			]
		},
		check_address: {
			identifier : "check_address",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your full address."
				}
			]
		},
	}, {
		inline : true,
		on : "blur"
	});
};


var form_wire = function() {
	$("form").form({
		wire_beneficiary_name: {
			identifier : "wire_beneficiary_name",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter the beneficiary's name."
				}
			]
		},
		wire_account_number: {
			identifier : "wire_account_number",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your account number."
				}
			]
		},
		wire_bank_name: {
			identifier : "wire_bank_name",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your bank's name."
				}
			]
		},
		wire_routing_aba_swift: {
			identifier : "wire_routing_aba_swift",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter the Routing / ABA / Swift."
				}
			]
		},
		wire_bank_address: {
			identifier : "wire_bank_address",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your bank's address."
				}
			]
		},
	}, {
		inline : true,
		on : "blur"
	});
};


var form_direct = function() {
	$("form").form({
		direct_account_holder: {
			identifier : "account_holder",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter the account holder's name."
				}
			]
		},
		direct_account_number: {
			identifier : "direct_account_number",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your account number."
				}
			]
		},
		direct_routing_number: {
			identifier : "direct_routing_number",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your bank's routing number."
				}
			]
		},
		direct_bank_name: {
			identifier : "direct_bank_name",
			rules: [
				{
					type   : "empty",
					prompt : "Please enter your bank's name."
				}
			]
		},
	}, {
		inline : true,
		on : "blur"
	});
};

set_invisible();

$(".payment.method").change(function() {
	set_invisible();
	$("#" + $(this).val()).show();

	switch($(this).val()) {
		case "check":
			form_check();
			break;

		case "wire":
			form_wire();
			break;

		case "direct":
			form_direct();
			break;

		default:
			form_paypal();
			return;
	}
});
