from lockers.utils import manage_url_patterns
from ..models import List


app_name = "lists"
urlpatterns = manage_url_patterns(List)
