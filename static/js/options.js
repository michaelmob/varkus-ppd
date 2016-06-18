var Options = function() { };
Options.callback = function() { };

Options.get = function(key, _default=null) {
	var value = localStorage.getItem("options:" + key);
	
	if(value == null && _default != null)
		return Options.set(key, _default);

	if(value == "disabled")
		return false;

	return value;
};

Options.set = function(key, value) {
	localStorage.setItem("options:" + key, value);
	return value;
};

Options.save = function() {
	$(".options.form .dropdown.option").each(function(i) {
		Options.set($(this).attr("id"),
			$(this).dropdown("get value") || $(this).attr("data-default"));
	});

	Options.callback();
};

Options.load = function(c) {
	$(".options.form .dropdown.option").each(function(i) {
		$(this).dropdown("set selected", 
			Options.get($(this).attr("id")) || $(this).attr("data-default"));
	});

	if(!!c) Options.callback = c;
	Options.callback();
};