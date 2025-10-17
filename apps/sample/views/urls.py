from django.urls import include, path

from . import HomeRedirectView, sign_out
from .sign_in import SignInView
from .home import urls as home_urls
from .user import urls as user_urls
from .post import urls as post_urls

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='root'),
    path('sign-in', SignInView.as_view(), name='sign_in'),
    path('sign-out', sign_out, name='sign_out'),
    path('home/', include(home_urls.__name__)),
    path('users/', include(user_urls.__name__)),
    path('posts/', include(post_urls.__name__)),
]