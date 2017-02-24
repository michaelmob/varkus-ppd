$("form.box").form({
	inline: true,
	fields: {
		name: "empty",
	}
});

var file_button = $("label[for='id_file'] span");
var button_text = file_button.text();
var file_upload_data = null;
var file_upload_settings = {
	dataType: "json",
	maxNumberOfFiles: 1,

	humanize: function(bytes) {
		var sizes = ["B", "KB", "MB", "GB", "TB"];
		if (bytes == 0) return "0B";
		var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
		return Math.round(bytes / Math.pow(1024, i), 2) + sizes[i];
	},

	remove: function(message) {
		file_button.text(button_text);
		$("#error-message").text(message);
		$(".ui.error.modal").modal("show");
	},

	add: function (e, data) {
		var file = data.files[0];
		file_upload_data = data;

		if(file.size > parseInt($("#id_file").attr("max-file-size")))
			return file_upload_settings.remove("File size is too large.");
	},

	error: function(e, data) {
		file_upload_settings.remove("Something went wrong. Please try again later.");
		setTimeout(function() {
			$(".upload.modal").modal("hide");
		}, 750);
	},

	done: function (e, data) {
		window.location = data.result.data.url;
	},

	progressall: function (e, data) {
		var percent = parseInt(data.loaded / data.total * 100);
		var p = file_upload_settings.humanize;

		$(".ui.progress").progress({ value: percent });
		$(".ui.progress>.label").html(p(data.loaded) + " / " + p(data.total));
	}
};


$(".upload.button").click(function(e) {
	if($("form.box").form("is valid"))
		file_upload_data.submit();
	e.preventDefault();
	return false;
});


$("#id_file").change(function() {
	var value = $(this).val();
	file_button.text(!value.startsWith("C:\\fakepath\\") ? value : value.substr(12));
	if(file_button.text() != button_text)
		$(".upload.button").removeClass("disabled");
	else
		$(".upload.button").addClass("disabled");
});


$("#id_file")
	.fileupload(file_upload_settings)
	.bind("fileuploadsubmit", function (e, data) {
		$(".upload.button").addClass("disabled");
		setTimeout(function() {
			$(".upload.button").removeClass("disabled");
		}, 2000);

		$(".ui.progress").progress({value: 0});
		$(".ui.upload.modal").modal("show");
		$(".file.name").html(data.files[0].name);

		data.formData = {
			"name": $("[name='name']").val(),
			"description": $("[name='description']").val(),
			"csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
		};
	});