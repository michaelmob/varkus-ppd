$(function() {
	$(".ui.modal.site.settings")
		.modal({
			onApprove: function() {
				Settings.save();
				return true;
			},
			onDeny: function() {
				Settings.load();
				return true;
			}
		})
		.modal("attach events", ".site.settings.item", "show");
});