from django.urls import path

from .views import PostViewSet

urlpatterns = [
    path('quotes', PostViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
]