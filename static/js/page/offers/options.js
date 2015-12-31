$(".remove.button").api({
	action: "set offer importance",
	urlData: {
		importance: "neutral"
	},
	onSuccess: function(response) {
		$(this).parent().parent().remove();
    }
});