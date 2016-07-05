$(".ui.modal.edit")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.button", "show");

$(".ui.modal.delete")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".delete.button", "show");

$(".ui.modal.embed")
	.modal("attach events", ".embed.button", "show");

$("form").form({
	inline : true,
	fields: {
		name: {
			identifier : "name",
			rules: [{
				type   : "empty",
				prompt : "Please enter a name for your widget"
			}]
		},
	}
});