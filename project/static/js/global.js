$(function() {
	$(".ui.dropdown").dropdown();
	$(".ui.checkbox").checkbox();
	
	$('.hover').popup({
		hoverable: true,
		position : 'top center',
		delay: { show: 0, hide: 0 }
	});

	$(".message .close").click(function() {
		$(this).closest(".message").slideUp(100);
	});

	$(".app.button").click(function() {
		$(".sidebar").sidebar("toggle");
	});

	$(window).resize(function() {
		$(".side.menu").height($(window).height() - $(".main.menu").height());
	});

	$(window).resize();
});