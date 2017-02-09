function Socket(url) {
	this.onOpen = function() {
		return undefined;
	};

	this.onClose = function(event) {
		return undefined;
	};

	this.onMessage = function(result) {
		console.log(result);
	};

	this.onError = function(event) {
		return undefined;
	};

	function initialize(_this) {
		var ws = new WebSocket(url);

		ws.onopen = function(event) {
			_this.onOpen(event);
		};

		ws.onclose = function() {
			ws = undefined;
			//initialize(_this);
			_this.onClose();
		};

		ws.onmessage = function(event) {
			try {
				_this.onMessage(JSON.parse(event.data));
			} catch (e) {
				return;
			}
		};

		ws.onerror = function(event) {
			_this.onError(event);
		};

		return ws;
	};

	initialize(this);
}