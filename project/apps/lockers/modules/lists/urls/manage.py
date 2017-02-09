from lockers.utils import manage_url_patterns
from modules.lists.models import List


urlpatterns = manage_url_patterns(List)
