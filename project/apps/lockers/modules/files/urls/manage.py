from lockers.utils import manage_url_patterns
from ..models import File


urlpatterns = manage_url_patterns(File)