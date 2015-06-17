$(".ui.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	name: {
		identifier : "name",
		rules: [
		{
			type   : "empty",
			prompt : "Please a name for your link."
		}
		]
	},

	item_name: {
		identifier : "url",
		rules: [
		{
			type   : "url",
			prompt : "Please enter a URL."
		}
		]
	},
}, {
	inline : true,
	on : "blur"
});