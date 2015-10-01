$(".ui.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	name: {
		identifier : "name",
		rules: [
		{
			type   : "empty",
			prompt : "Please enter a name for your link."
		}
		]
	},

	url: {
		identifier : "url",
		rules: [
		{
			type   : "empty",
			prompt : "Please enter a URL."
		}
		]
	},
}, {
	inline : true,
	on : "blur"
});