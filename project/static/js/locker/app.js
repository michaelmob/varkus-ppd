var socket = null;
var openSocket = function() {
	if(!!socket)
		return;

	socket = new Socket(obj[0]);
	socket.onMessage = function(result) {
		if(!result.success) {
			return;
		}

		var a = result.type == "UNLOCK";
		var b = result.data.locker == obj[1];
		var c = result.data.code == obj[2]

		if(a && b && c) {
			window.location = result.data.url;
		}

		else if(result.type == "CLICK") {
			document.querySelector(".message").innerHTML = result.message;

			if (parseInt(document.getElementById("amount").innerHTML) < 1) {
				window.location.reload();
			}
		}
	};
};


if(typeof immediateOpen === "boolean" && immediateOpen) {
	openSocket();
}


var items = document.querySelectorAll(".widget .item");
for (var i = 0; i < items.length; i++) {
	items[i].onclick = function() {
		document.querySelector(".indicator").style.display = "block";
		openSocket();
	};
}
