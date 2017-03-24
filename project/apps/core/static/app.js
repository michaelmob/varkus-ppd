$(function() {
	$(".ui.dropdown").dropdown();
	$(".ui.checkbox").checkbox();

	$(".popup").popup({
		hoverable: true,
		position : "top center",
		delay: {
			show: 0, hide: 0
		}
	});

	$(".message .close").on("click", function() {
		$(this).closest(".message").slideUp(100);
	});

	$(".ui.sidebar").sidebar({
		scrollLock: true
	}).sidebar("attach events", ".app.item");

});

$.fn.api.settings.api = {
	"offer priority": "/offers/{id}/priority/",
	"offer boost": "/offers/{id}/boost/",
	"offer reset": "/offers/{id}/reset/",
	"ticket status": "/tickets/{id}/{status}/",
	"post delete": "/tickets/{id}/delete/",
};