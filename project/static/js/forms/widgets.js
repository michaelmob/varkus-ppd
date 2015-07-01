$(".ui.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	name: {
		identifier : "name",
		rules: [
		{
			type   : "empty",
			prompt : "Please a name for your widget."
		}
		]
	}
}, {
	inline : true,
	on : "blur"
});