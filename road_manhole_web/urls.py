from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户管理相关的URL
    path('api/user/', include('accounts.urls')),
    # DRF提供的Token认证机制
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
