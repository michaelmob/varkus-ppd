var socket = null;
var openSocket = function() {
	if(!!socket)
		return;

	socket = WS4Redis({
		uri: uri + "locker?subscribe-session",
		heartbeat_msg: "PING",
		receive_message: function(data) {
			data = $.parseJSON(data);

			if(!data.success)
				return;

			if(data.data.locker == locker && data.data.code == code)
				window.location = data.data.url;
		},
	});
};

var items = document.querySelectorAll(".widget .item");

for (var i = 0; i < items.length; i++) {
	items[i].onclick = function() {
		document.querySelector(".progress.indicator").style.display = "block";
		openSocket();
	};

	items[i].onmouseover = function(e) {
		if(e.target.className == "item")
			return;

		var node = document.createElement("p");
		node.className += "popup";
		node.textContent = e.target.parentNode.getAttribute("data-content");

		e.target.parentNode.appendChild(node);
	};

	items[i].onmouseout = function(e) {
		e.target.parentNode.querySelector(".widget .popup").remove();
	};
}
