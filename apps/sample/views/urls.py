from django.urls import include, path

from . import index
urlpatterns = [
    path('', index, name='index'),
    path('home/', include('sample.views.home.urls')),
    path('users/', include('sample.views.user.urls')),
    path('posts/', include('sample.views.post.urls')),
]