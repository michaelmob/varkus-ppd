var setProgress = function(x) {
	document.querySelector(".progress.indicator")
		.style.display = x ? "block" : "none";
};

var socket = null;
var openSocket = function() {
	if(!!socket)
		return;

	setProgress(true);

	socket = WS4Redis({
		uri: uri + "locker?subscribe-session",
		heartbeat_msg: "--heartbeat--",
		receive_message: function(data) {
			data = $.parseJSON(data);

			if(!data.success)
				return;

			if(data.data.locker == locker &&
				data.data.code == code) {
				window.location = data.data.url;
			}
		},
	});
};

var items = document.querySelectorAll(".w .item");
for(var i = 0; i < items.length; i++) {
	items[i].onclick = openSocket;
}