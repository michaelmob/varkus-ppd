/* Editor */
var editor = ace.edit("editor");
editor.getSession().setMode("ace/mode/css");


/* Preview */
$(".preview .progress.indicator").css("display", "block");


/* Tabs */
var activeTab = null;
var tabMenu = $(".ui.right.menu .item");
var continueButton = $(".continue.button");
var buttonIcon = continueButton.children(".icon");
var buttonText = continueButton.children("span");

tabMenu.tab({ 
	onLoad: function(tabName) {
		activeTab = tabName;

		if (tabName != "preview") {
			buttonIcon.removeClass("checkmark").addClass("arrow right");
			buttonText.text("Continue");
			return;
		}

		buttonIcon.removeClass("arrow right").addClass("checkmark");
		buttonText.text("Save");

		// Prepend ".preview" to the beginning of the selector
		var css = editor.getValue()
			.replace(/([^\r\n,{}]+)(,(?=[^}]*{)|\s*{)/gm, ".preview $&")
			.replace(/^.preview @/g, "@");

		// Re-create preview-css style tag
		$("#preview-css").remove();
		$("head").append("<style id=\"preview-css\">" + css + "</style>");
	}
});

tabMenu.tab("change tab", editor.getValue().length < 1 ? "styler" : "css");


/* Form Submission */
$(".continue.button").click(function() {
	switch (activeTab) {
		case "preview":
			$("[name=\"content\"]").val(editor.getValue());
			$("form.update").submit();
			return;

		case "styler":
			$.get("/static/widgets/user.template", function(data) {
				var match, regex = /(\$([A-z0-9\-]+))[\W]/g;
				while (match = regex.exec(data)) {
					var selector = "#" + match[2];
					var value = $(selector).val() || $(selector).attr("placeholder");
					value = value.replace(/\"/g, "");

					data = data.replace(RegExp("\\" + match[1], "i"), value);
				}

				var categoryIcons = $("#category-icons").is(":checked");
				var priorityIcons = $("#priority-icons").is(":checked");
				var props = " {\n\tdisplay:none;\n}"

				if (!categoryIcons && !priorityIcons)
					data += "\n\n.widget .icon.wrapper" + props
				else {
					if (!categoryIcons)
						data += "\n\n.widget .icon.wrapper:not(.priority)" + props

					if (!priorityIcons)
						data += "\n\n.widget .priority.icon.wrapper" + props
				}

				editor.setValue(data, 1);
			});

			tabMenu.tab("change tab", "css");
			break;

		default:
			tabMenu.tab("change tab", "preview");
	}
});