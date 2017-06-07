/*
* Priority Popup Menu
*/
$(".priority.item").popup({
	popup: ".priority.popup",
	on: "click",
	position: "bottom right",
	hoverable: true,
	delay: {
		show: 50,
		hide: 150000
	},
});

/*
* Offer Removal Button
*/
$(".remove.offer.button").api({
	method: "POST",
	action: "offer priority",
	beforeSend: function(settings) {
		settings.data.value = "neutral";
		return settings;
	},
	onSuccess: function(response) {
		$(this).parent().parent().remove();
	}
});


/*
* Offer Boost Button
*/
$(".boost.label").api({
	method: "POST",
	action: "offer boost",
	onSuccess: function(response) {
		$(this).state('flash text', '+10').transition("pulse");
	}
}).popup({
	title: "Boost Offer",
	content: "Boost this offer to the top of the offer wall for 10 clicks"
});


/*
* Offer Reset Button
*/
$(".reset.offer.button").api({
	method: "POST",
	action: "offer reset",
	onSuccess: function(response) {
		$(this).parent().parent().remove();
	}
});