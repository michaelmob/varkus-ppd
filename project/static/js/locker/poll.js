var _s_pollInterval, _s_idleInterval;
var _s_idleSeconds = 0;

function _s_poll(uri) {
	if(_s_idleSeconds > 900)
		return;

	var request = new XMLHttpRequest();
	request.open('GET', uri, true);

	request.onload = function () {
		if (request.status >= 200 && request.status < 400) {
			clearInterval(_s_pollInterval);
			window.location = request.responseText;
		}
	};

	request.send();
}

function _s_idle() {
	_s_idleSeconds = document.hidden ? _s_idleSeconds + 1 : 0;
}

function _s_start(uri) {
	_s_pollInterval = setInterval("_s_poll(\"" + uri + "\");", 15 * 1000);
	_s_pollInterval = setInterval(_s_idle, 1000);
}