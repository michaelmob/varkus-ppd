$(".ui.sortable.table th.orderable").click(function() {
	window.location = $(this).find("a").attr("href");
	return false;
});
$("th.desc,th.asc").addClass("sorted");

$(".ui." + n + ".pagination").twbsPagination({
	startPage: s,
	totalPages: t,
	onPageClick: function(event, page) {
		$("." + n + ".dimmer").addClass("active");
	}
});