var toggle = true;
var title = document.title;

setInterval(function() {
	if(!document.hasFocus()) {
		document.title = toggle ? "◦ " + title : "• " + title;
		toggle = !toggle;
	}
	else
		document.title = title;
}, 500);