var setupTable = function() {
	$(".ui.sortable.table th").click(function() {
		var link = $(this).find("a");
		if(link.length)
			window.location = link.attr("href");
		return false;
	});

	$(".ui.pagination .item").click(function() {
		$(this).siblings(".item").removeClass("active");
		$(this).addClass("active");
		$(this).parent().siblings(".table").children(".dimmer").addClass("active");
	});
};

setupTable();