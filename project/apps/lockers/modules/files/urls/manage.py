from lockers.utils import manage_url_patterns
from ..models import File


app_name = "files"
urlpatterns = manage_url_patterns(File)