var _cb_interval = 0;

var _cb_request = function(url) {
	$.get(url, function(data) {
		if((data != "0") && (data.indexOf("/") > -1)) {
			clearInterval(_cb_interval);
			window.location = data;
		}
	});
};

var _cb_request_start = function(url) {
	_cb_interval = setInterval("_cb_request(\"" + url + "\");", 15 * 1000);
};

var _cb_request_stop = function() {
	clearInterval(_cb_interval);
};

$(".cb.wrap>a").click(function() {
	$(".progress.indicator").show();
});