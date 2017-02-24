new Clipboard(".copy.button");

$(".copy.button").state({
	onActivate: function() {
		$(this).state("flash text");
	},
	text: {
		flash: "<i class=\"copy icon\"></i> Copied!"
	}
});