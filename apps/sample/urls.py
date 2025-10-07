from django.urls import include, path

urlpatterns = [
    path('', include('sample.views.urls')),
]