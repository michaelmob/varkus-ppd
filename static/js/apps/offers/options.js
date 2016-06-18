$(".remove.button").api({
	action: "offer importance",
	urlData: {
		importance: "neutral"
	},
	onSuccess: function(response) {
		$(this).parent().parent().remove();
    }
});