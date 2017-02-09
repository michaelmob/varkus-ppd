$("form").form({
	inline : true,
	fields: {
		subject: {
			identifier : "subject",
			rules: [{
				type   : "empty",
				prompt : "Please enter your subject"
			}, {
				type   : "maxLength[100]",
				prompt : "A maximum of 100 characters may be used"
			}]
		},
		priority: {
			identifier : "priority",
			rules: [{
				type   : "empty",
				prompt : "Please select a priority"
			}]
		},
		category: {
			identifier : "category",
			rules: [{
				type   : "empty",
				prompt : "Please select a category"
			}]
		},
		message: {
			identifier : "message",
			rules: [{
				type   : "empty",
				prompt : "Please enter your message"
			}, {
				type   : "maxLength[5000]",
				prompt : "A maximum of 5000 characters may be used"
			}]
		},
	}
});


$("#id_file").change(function() {
	var value = $(this).val();
	value = !value.startsWith("C:\\fakepath\\") ? value : value.substr(12);
	$("label[for='id_file'] span").text(value);
});