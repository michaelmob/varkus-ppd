from .utils import validate_file
from viking.utils.constants import DEFAULT_BLANK_NULL


FILE_KWARGS = {
	"upload_to": "reports/%Y/%m/",
	"validators": [validate_file],
	**DEFAULT_BLANK_NULL
}