from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from inference import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户管理相关的URL
    # path('api/user/', include('accounts.urls')),
    # DRF提供的Token认证机制
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', views.upload_and_infer, name='upload_and_infer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
