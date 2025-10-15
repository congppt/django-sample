from django.urls import reverse
from django.views.generic import RedirectView


class HomeRedirectView(RedirectView):
    pattern_name = 'login'
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('home')
        return super().get_redirect_url(*args, **kwargs)