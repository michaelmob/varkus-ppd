$(function() {
	/*var resizeInterval;
	var sideMenu = $(".ui.left.fixed.menu");

	var doResize = function() {
		if ($(window).width() < 992) {
			if(!sideMenu.hasClass("sidebar"))
				sideMenu.addClass("sidebar");
		} else {
			if(sideMenu.hasClass("sidebar"))
				sideMenu.removeClass("sidebar");
		}
	};

	window.onresize = function(){
		clearTimeout(resizeInterval);
		resizeInterval = setTimeout(doResize, 50);
	};*/
	
	window.dispatchEvent(new Event("resize"));
});