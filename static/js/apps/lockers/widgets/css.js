var editor = ace.edit("editor");
editor.getSession().setMode("ace/mode/css");

$("form").on("submit", function(e) {
	$("[name='content']").val(editor.getValue());
});