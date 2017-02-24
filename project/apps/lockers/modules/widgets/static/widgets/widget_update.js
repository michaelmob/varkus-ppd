$(".ui.secondary.right.menu .item").tab({
	onVisible: function(tabPath) {
		var el = $("[data-tab-information='" + tabPath + "']");
		el.addClass("active");
		el.siblings(".active").removeClass("active");
	}
})


if (document.location.href.indexOf("#") >= 0) {
	var tab_name = document.location.href.split("#")[1]
	$(".ui.secondary.right.menu .item").tab("change tab", tab_name);
}