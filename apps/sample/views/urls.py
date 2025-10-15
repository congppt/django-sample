from django.urls import include, path

from . import HomeRedirectView
from .login import LoginView
from .home import urls as home_urls
from .user import urls as user_urls
from .post import urls as post_urls

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='root'),
    path('login', LoginView.as_view(), name='login'),
    path('home/', include(home_urls.__name__)),
    path('users/', include(user_urls.__name__)),
    path('posts/', include(post_urls.__name__)),
]