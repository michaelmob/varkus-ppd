$(function() {
	/* Semantic UI */
	$(".ui.dropdown").dropdown();

	$(".ui.checkbox").checkbox();

	$(".popup").popup({ hoverable: true,
		position : "top center",
		delay: { show: 0, hide: 0 } });

	$(".message .close").on("click", function() {
		$(this).closest(".message").slideUp(100); });

	$(".ui.sidebar").sidebar("attach events", ".hamburger.icon");
});