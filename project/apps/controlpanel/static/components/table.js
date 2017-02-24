$(".ui.sortable.table th").click(function() {
	var link = $(this).find("a");
	if(link.length)
		window.location = link.attr("href");
	return false;
});

$(".ui.pagination .item").click(function() {
	var e = $(this);
	e.siblings(".item").removeClass("active");
	e.addClass("active");
	e.parent().siblings(".table").children(".dimmer").addClass("active");
});