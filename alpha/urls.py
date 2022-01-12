from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet, create_auth, create_api_key

urlpatterns = [
    path('quotes', PostViewSet.as_view({
        'get': 'list',
        'post': 'force_fetch'
    })),
    path('latest_quote', PostViewSet.as_view({
        'get': 'retrieve',
    })),
    path('get-token', obtain_auth_token, name='get_auth_token'),
    path("create_user", create_auth, name="create_user"),
    path("create_api_key", create_api_key, name="create_api_key")
]