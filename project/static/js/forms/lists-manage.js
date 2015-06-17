/*var rows = "";

var positive = "<i class='primary check icon'></i>";
var negative = "<i class='primary cancel icon'></i>";

for(var i = 0; i < items.length; i++) {
	rows += "<tr><td>" + items[i][0] + "</td>";
	rows += "<td class='right aligned'>" + (items[i][1] == 0 ? positive : negative) + "</td></tr>";
}

$(".table.items>tbody").html(rows);
$(".dimmer").removeClass("active");*/

$(".ui.modal.edit")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".edit.button", "show");

$(".ui.modal.delete")
	.modal({onApprove: function() { return false; }})
	.modal("attach events", ".delete.button", "show");

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