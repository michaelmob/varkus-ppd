from lockers.utils import locker_url_patterns
from ..models import File


app_name = "file"
urlpatterns = locker_url_patterns(File)