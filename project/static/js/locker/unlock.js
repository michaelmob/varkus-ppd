var toggle = true;
var title = document.title;

setInterval(function() {
	if(!document.hasFocus()) {
		document.title = toggle ? "_ Unlocked ‾" : "‾ Unlocked _";
		toggle = !toggle;
	}
	else
		document.title = title;
}, 500);