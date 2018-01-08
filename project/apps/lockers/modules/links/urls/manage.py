from lockers.utils import manage_url_patterns
from ..models import Link


app_name = "links"
urlpatterns = manage_url_patterns(Link)
