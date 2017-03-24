document.addEventListener("DOMContentLoaded", function() {
	// Query for all Widgets
	var widgets = document.querySelectorAll("iframe[code]");
	if (widgets.length < 1)
		return;

	// Add iframeResizer script to <head> tag
	var head = document.getElementsByTagName("head")[0];
	if (head) {
		// Create script tag for iframeResizer (parent)
		// This allows automatic resizing of the iframe for a native look
		var script = document.createElement("script");
		script.onload = function() {
			var opts = {"heightCalculationMethod": "documentElementOffset"};
			for (var i = widgets.length - 1; i >= 0; i--)
				iFrameResize(opts, widgets[i]);
		};
		script.src = "https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.5.11/iframeResizer.min.js";
		head.appendChild(script);
	}

	// Get <script> src
	var scriptSrc, script = document.querySelector("script[src$='widgets/external.min.js']");
	if (script)
		scriptSrc = script.src.split("/").splice(0, 3).join("/");

	// Set sources for iframes
	for (var i = widgets.length - 1; i >= 0; i--) {
		var src = widgets[i].getAttribute("from") || scriptSrc || "https://varkus.com";
		var url = widgets[i].getAttribute("url") || document.location.href.split("#")[0];
		var id, code = widgets[i].getAttribute("code");

		// Find visitor ID
		if (window["id_" + code])
			id = window["id_" + code];
		else if (matches = document.location.href.match(/\#([0-9]+)$/g))
			id = matches[0].substring(1);

		// Build visitor URL
		src = [src.replace(/\/$/, ""), "widget", code];
		if (id)
			src.push(id);

		widgets[i].src = src.join("/") + "/?url=" + url;
	}
}, false);