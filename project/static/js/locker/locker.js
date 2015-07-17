var _s_uri, _s_pollInterval, _s_idleInterval, _s_idleSeconds = 0;
var _s_confirmLeave = false;

function _s_poll(uri) {
	if(_s_idleSeconds > 900)
		return;

	var request = new XMLHttpRequest();
	request.open('GET', uri, true);

	request.onload = function () {
		if (request.status >= 200 && request.status < 400) {
			_s_stop();
			window.location = request.responseText;
		}
	};

	request.send();
}

function _s_idle() {
	_s_idleSeconds = document.hidden ? _s_idleSeconds + 1 : 0;
}

function _s_set(uri) {
	_s_uri = uri;
}

function _s_start() {
	_s_confirmLeave = true;
	_s_pollInterval = setInterval("_s_poll(\"" + _s_uri + "\");", 5 * 1000);
	_s_idleInterval = setInterval(_s_idle, 1000);
	_s_progressShow();
}

function _s_stop() {
	_s_confirmLeave = false;
	clearInterval(_s_pollInterval);
	clearInterval(_s_idleInterval);
	_s_progressHide();
}

function _s_warning(e) {
	if(!_s_confirmLeave)
		return;

	if(!e)
		e = window.event;

	e.cancelBubble = true;
	e.returnValue = "Are you sure you want to leave this page?";

	if (e.stopPropagation) {
		e.stopPropagation();
		e.preventDefault();
	}
}

var _s_progressIndicator = document.querySelector(".progress.indicator");
function _s_progressShow() { _s_progressIndicator.style.display = "block"; }
function _s_progressHide() { _s_progressIndicator.style.display = "none"; }

function _s_paginator(items, per, container) {
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

var _s_offers = document.querySelectorAll(".s.wrap>a");

for(var i = 0; i < _s_offers.length; i++)
	_s_offers[i].onclick = _s_start;

new _s_paginator(_s_offers, 5, document.querySelector(".ui.pagination"));

window.onbeforeunload = _s_warning;