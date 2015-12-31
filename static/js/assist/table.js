$(".ui.sortable.table th.sortable").click(function() {
	window.location = $(this).find("a").attr("href"); return false;
});
$("th.desc").addClass("sorted descending");
$("th.asc").addClass("sorted ascending");
