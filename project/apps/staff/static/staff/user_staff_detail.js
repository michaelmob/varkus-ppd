$(".recalculate.button").api({
	url: "?action=recalculate",
	onSuccess: function(response) {
		$(this).state("flash text", "Success!");
	},
});