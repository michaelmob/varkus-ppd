$(".ui.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	inline : true,
	fields: {
		name: {
			identifier : "name",
			rules: [{
				type   : "empty",
				prompt : "Please enter a name for your widget"
			}]
		}
	}
});