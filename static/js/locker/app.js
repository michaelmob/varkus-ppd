var socket = null;
var openSocket = function() {
	if(!!socket)
		return;

	socket = new Socket(obj[0]);
	socket.onMessage = function(result) {
		if(!result.success)
			return;

		if(result.data.locker == obj[1] && result.data.code == obj[2])
			window.location = result.data.url;
	};
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
