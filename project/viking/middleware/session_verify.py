from apps.user.models import Party

class SessionVerifyMiddleware(object):
    def process_request(self, request):
        """ Create Session if nonexistent and verify user defaults """
        if not request.session.exists(request.session.session_key):
            request.session.create()

        if request.user.is_authenticated() and not request.user.profile.party:
            request.user.profile.party = Party.default()
