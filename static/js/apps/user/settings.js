new Clipboard(".copy.button");

$(".copy.button").state({
	onActivate: function() {
		$(this).state("flash text");
	},
	text: {
		flash: "<i class='copy icon'></i> Copied!"
	}
});

$(".ui.modal").modal({
	onApprove: function() {
		return false; 
	}
});

$(".ui.modal.account").form({
	inline : true,
	fields: {
		email: {
			identifier : "email",
			rules: [{
				type   : "email",
				prompt : "Please enter your e-mail address"
			}]
		}
	}
}).modal("attach events", ".edit.account", "show");

$(".ui.modal.personal").form({
	inline : true,
	fields: {
		first_name: {
			identifier: "first_name",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your first name"
			}]
		},
		last_name: {
			identifier: "last_name",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your last name"
			}]
		},
		phone_number: {
			identifier: "phone_number",
			rules: [{
				type	: "regExp[^[\-\+ 0-9]+$]",
				prompt	: "Please enter your phone number"
			}]
		},
		address: {
			identifier: "address",
			rules: [{
				type	: "minLength[3]",
				prompt	: "Please enter your address"
			}]
		},
		city: {
			identifier: "city",
			rules: [{
				type	: "minLength[2]",
				prompt	: "Please enter your city"
			}]
		},
		state: {
			identifier: "state",
			rules: [{
				type	: "minLength[3]",
				prompt	: "Please enter your state or region"
			}]
		},
		country: {
			identifier: "country",
			rules: [{
				type	: "minLength[1]",
				prompt	: "Please select your country"
			}]
		},
		postal_code: {
			identifier: "postal_code",
			rules: [{
				type	: "empty",
				prompt	: "Please enter your postal code"
			}]
		},
	}
}).modal("attach events", ".edit.personal", "show");