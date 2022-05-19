from django.urls import path

from api.views import ShortUrlView, OriginalUrlView

app_name = 'api'

urlpatterns = [
    path('get-short-url/', ShortUrlView.as_view(), name='get-short-url'),
    path('get-original-url/', OriginalUrlView.as_view(), name='get-original-url'),
]
