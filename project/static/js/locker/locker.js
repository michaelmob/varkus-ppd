function Poll(url) {
	var self = this;
	this.idleInteval = undefined;
	this.pollInterval = undefined;
	this.idleSeconds = 0;
	this.confirmLeave = false;

	this.sendRequest = function() {
		if(self.idleSeconds > 900)
			return;

		var request = new XMLHttpRequest();
		request.open("GET", url, true);

		request.onload = function () {
			if (request.status >= 200 && request.status < 400) {
				self.stop();
				window.location = request.responseText;
			}
		};

		request.send();
	};

	this.start = function() {
		self.stop();

		self.confirmLeave = true;
		window.onbeforeunload = self.warning;

		clearInterval(self.pollInterval);
		clearInterval(self.idleInterval);

		self.pollInterval = setInterval(function() { self.sendRequest() }, 5 * 1000);
		self.idleInterval = setInterval(function() { self.idleSeconds = document.hidden ? self.idleSeconds + 1 : 0; }, 1000);
		showProgress();
	};

	this.stop = function() {
		self.confirmLeave = false;
		clearInterval(self.pollInterval);
		clearInterval(self.idleInterval);
		hideProgress();
	};

	this.warning = function(e) {
		if(!self.confirmLeave)
			return;

		if(!e) e = window.event;

		e.cancelBubble = true;
		e.returnValue = "Are you sure you want to leave this page?";

		if (e.stopPropagation) {
			e.stopPropagation();
			e.preventDefault();
		}
	};
}

var progressIndicator = document.querySelector(".progress.indicator");
function showProgress() { progressIndicator.style.display = "block"; }
function hideProgress() { progressIndicator.style.display = "none"; }

function Paginator(items, per, container) {
	this.items = items;
	this.container = container;
	this.pages = Math.round(this.items.length / per);
	this.buttons = [];
	
	this.hideItems = function() {
		for(var i = 0; i < this.items.length; i++) {
			this.items[i].style.display = "none";
		}
	};

	this.showPage = function(num) {
		this.hideItems();
		var start = per * (num - 1);
		for(var i = start; i < (start + per); i++) {
			this.items[i].style.display = "";
		}
	};

	this.notAction = function() {
		for(var i = 0; i < this.buttons.length; i++) {
			this.buttons[i].className = "item";
		}
	};

	this.create = function() {
		this.buttons = [];
		var _this = this;
		
		if(this.pages <= 1) {
			this.container.style.display = "none";
			return;
		}

		for(var i = 1; i < this.pages + 1; i++) {
			var el = document.createElement("a");
			el.setAttribute("class", "item");
			el.setAttribute("page", i);
			el.innerHTML = i.toString();
			
			el.onclick = function() {
				_this.notAction();
				_this.showPage(this.getAttribute("page"));
				this.className = "item active";
			};
			
			this.container.appendChild(el);
			this.buttons.push(el);
		}
	};
	
	this.create();
	this.buttons[0].className = "item active";
	this.showPage(1);
}

var offers = document.querySelectorAll(".s.wrap>a");
poll = new Poll(pollUrl);

for(var i = 0; i < offers.length; i++)
	offers[i].onclick = poll.start;

new Paginator(offers, 5, document.querySelector(".ui.pagination"));