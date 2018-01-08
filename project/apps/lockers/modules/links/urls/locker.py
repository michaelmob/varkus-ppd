from lockers.utils import locker_url_patterns
from ..models import Link


app_name = "link"
urlpatterns = locker_url_patterns(Link)