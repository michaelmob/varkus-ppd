$(function() {
	$(".ui.options.modal").modal("attach events", ".options.item", "show");

	var optionsList = ["accept-messages", "notification-sound"];

	var loadOptions = function() {
		if(localStorage.options == undefined)
			saveOptions();

		$.each(optionsList, function(val) {
			$(".options.form #" + val).val(localStorage.getItem("opt_" + val));
		});
	};

	var saveOptions = function() {
		$.each(optionsList, function(val) {
			localStorage.setItem("opt_" + val, $(".options.form #" + val).val());
		});
	};

	$(".save.options.button").click(function() {
		saveOptions();
	});

	loadOptions();
});