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
$(".boost.offer.button").api({
	method: "POST",
	action: "offer boost",
	onSuccess: function(response) {
		$(this).transition("tada");
	}
}).popup({
	title: "Boost",
	content: "Boosting this offer will ensure that it gets 10 clicks."
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