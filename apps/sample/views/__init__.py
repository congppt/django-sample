from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import RedirectView


class HomeRedirectView(RedirectView):
    pattern_name = 'sign_in'
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('home')
        return super().get_redirect_url(*args, **kwargs)

def sign_out(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất')
    return redirect('sign_in')