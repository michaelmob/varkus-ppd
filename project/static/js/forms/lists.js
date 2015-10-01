$(".ui.modal")
	.modal({ onApprove: function() { return false; } })
	.modal("attach events", ".create.button", "show");

$("form").form({
	name: {
		identifier : "name",
		rules: [
		{
			type   : "empty",
			prompt : "Please enter a name for your list."
		}
		]
	},

	item_name: {
		identifier : "item_name",
		rules: [
		{
			type   : "empty",
			prompt : "Please enter a name for an individual list item."
		}
		]
	},

	items: {
		identifier : "items",
		rules: [
		{
			type   : "empty",
			prompt : "Please insert list items."
		},
		{
			type   : "maxLength[5000]",
			prompt : "A maximum of 5000 characters may be used."
		}
		]
	},

	delimeter: {
		identifier : "delimeter",
		rules: [
		{
			type   : "empty",
			prompt : "Please choose a valid delimeter."
		}
		]
	},

	order: {
		identifier : "order",
		rules: [
		{
			type   : "empty",
			prompt : "Please choose a valid distribution order."
		}
		]
	}
}, {
	inline : true,
	on : "blur"
});