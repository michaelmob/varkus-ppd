$("form.box").form();

$("#id_file").change(function() {
	var value = $(this).val();
	value = !value.startsWith("C:\\fakepath\\") ? value : value.substr(12);
	$("label[for='id_file'] span").text(value);
});