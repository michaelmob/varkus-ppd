/*
* Extend the Audio class with helper functions
*/
Audio.prototype.addSound = function(value) {
	var opt = Settings.get(value + "-sound");

	if(!opt || opt == "disabled")
		return;

	this.sounds[value] = new Audio("/static/sounds/" + opt + ".mp3");
};

Audio.prototype.initiate = function() {
	this.sounds = {};
	this.addSound("conversion");
	this.addSound("large-conversion");
	this.addSound("click");

	return this;
};

Audio.prototype.playSound = function(value) {
	var sound = this.sounds[value] || null;

	if (sound)
		sound.play();
};

Audio.prototype.playConversion = function(largeConversion = false) {
	this.playSound(largeConversion ? "large-conversion" : "conversion");
};

Audio.prototype.playClick = function() {
	this.playSound("click");
};


/*
* Elements
*/
$(function() {
	$(".play.button").click(function() {
		var value = $(this).siblings(".option").dropdown("get value");

		if(!value || value == "disabled")
			return;

		new Audio("/static/sounds/" + value + ".mp3").play();
	});
});