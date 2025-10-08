from django.urls import include, path

from . import index, example_table_view
urlpatterns = [
    path('', index, name='index'),
    path('home/', include('sample.views.home.urls')),
    path('users/', include('sample.views.user.urls')),
    path('posts/', include('sample.views.post.urls')),
    path('test/', example_table_view.example_table_view, name='example_table_view'),
]