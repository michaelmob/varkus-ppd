import django_tables2 as tables

class Table_Base:
	class Meta:
		attrs = {
			"class": "ui sortable table",
			"th": {
				"_ordering": {
					"orderable": "sortable",
					"descending": "sorted descending",
					"ascending": "sorted ascending",
				}
			}
		}