from django.urls import path
from .views import UserAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user/<str:action>/', UserAPI.as_view(), name='user-api'),
    path('user/<str:action>/<int:pk>/', UserAPI.as_view(), name='user-api-with-pk'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
