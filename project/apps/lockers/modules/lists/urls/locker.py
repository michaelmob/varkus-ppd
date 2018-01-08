from lockers.utils import locker_url_patterns
from ..models import List


app_name = "list"
urlpatterns = locker_url_patterns(List)