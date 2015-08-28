$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results == null ? null : results[1] || 0;
}

$(".staff .item").click(function(e) {
	$(".staff .item").removeClass("active");
	$(this).addClass("active");

	$("iframe").attr("src", $(this).attr("href"));
	
	e.preventDefault();
	return;
});

$("iframe")
	.attr("src", decodeURIComponent($.urlParam("url") || "/admin/auth/user/"))
	.on("load", function()
{
	// Remove Django Header
	var contents = $(this).contents();
	contents.find("#header").remove();
	contents.find(".breadcrumbs a:lt(2)").remove();
	contents.find(".breadcrumbs").html(
		contents.find(".breadcrumbs").html().slice(7)
	);

	// Get iframe pathname, but only the first 4 of them
// for the link finding otherwise the wrong url is sent
	// and the tab won't get activated
	var iframePath = contents.get(0).location.pathname;
	var iframePath2 = (iframePath.split("/").splice(0, 4)).join("/")

	// Set tab active
	$(".tabular .item").removeClass("active");
	$("a[href*='" + iframePath2 + "']").addClass("active");

	// Set URL with iframe path so we can refresh/save link
	window.history.replaceState({} , "", "?url=" + iframePath);

	// Set height of frame segment to iframe's content height
	$(".frame.segment").height(contents.find("body").height());

	// Add options to model admin pages
	switch(contents.find("h1").text()) {
		case "Change user": userOptions(contents); break;
		case "Select lead to change": leadOptions(contents); break;

		case "Change widget": lockerOptions(contents, "WIDGET"); break;
		case "Change file": lockerOptions(contents, "FILE"); break;
		case "Change link": lockerOptions(contents, "LINK"); break;
		case "Change list": lockerOptions(contents, "LIST"); break;
	}

	// Change View site link to open new tab
	contents.find(".viewsitelink").click(function(e) {
		window.open($(this).attr("href"));
		e.preventDefault();
		return;
	});
});

var userOptions = function(contents) {
	var id = contents.find("#id_profile-0-user").val();
	$("h1", contents).append(
		"<small style='font-size:12px'> <a href='/admin/leads/lead/?user=" + id + "'>[Leads]</a>" +
		" <a href='/admin/widgets/widget/?user=" + id + "'>[Widgets]</a>" +
		" <a href='/admin/files/file/?user=" + id + "'>[Files]</a>" +
		" <a href='/admin/links/link/?user=" + id + "'>[Links]</a>" +
		" <a href='/admin/lists/list/?user=" + id + "'>[Lists]</a>" +
		" <a href='/admin/billing/invoice/?user=" + id + "'>[Invoices]</a></small>"
	);
};

var leadOptions = function(contents) {
	var id = contents.find("#id_profile-0-user").val();

	$.each(deposits, function(key, value) { 
		$("h1", contents).append(" <a style='font-size:12px' href='/admin/leads/lead/?deposit=" + value + "'>[" + key + "]</a> ");
	});
};

var leadOptions = function(contents) {
	var id = contents.find("#id_profile-0-user").val();

	$.each(deposits, function(key, value) { 
		$("h1", contents).append(" <a style='font-size:12px' href='/admin/leads/lead/?deposit=" + value + "'>[" + key + "]</a> ");
	});
};

var lockerOptions = function(contents, locker) {
	var id = contents.find("#id_profile-0-user").val();
	var code = $("#id_code", contents).val();
	$("h1", contents).append(
		"<small style='font-size:12px'> <a href='/admin/leads/lead/?locker=" + locker + "&locker_code=" + code + "'>[Leads]</a></small>"
	);
};