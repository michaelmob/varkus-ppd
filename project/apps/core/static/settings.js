var Settings = function() { };
Settings.callback = function() { };


Settings.get = function(key, _default=null) {
	var value = localStorage.getItem("settings:" + key);
	
	if(value == null && _default != null)
		return Settings.set(key, _default);

	if(value == "disabled")
		return false;

	return value;
};


Settings.set = function(key, value) {
	localStorage.setItem("settings:" + key, value);
	return value;
};


Settings.save = function() {
	$(".settings.form .dropdown.option").each(function(i) {
		Settings.set($(this).attr("id"),
			$(this).dropdown("get value") || $(this).attr("data-default"));
	});

	Settings.callback();
	return true;
};


Settings.load = function(c) {
	$(".settings.form .dropdown.option").each(function(i) {
		$(this).dropdown("set selected", 
			Settings.get($(this).attr("id")) || $(this).attr("data-default"));
	});

	if(!!c) Settings.callback = c;
	Settings.callback();
	return true;
};