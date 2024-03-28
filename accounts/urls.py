from django.urls import path
from .views import UserAPIView as UserAPI

urlpatterns = [
    # 用户注册、登录、注销等操作
    path('user/', UserAPI.as_view(), name='user-api'),
]

