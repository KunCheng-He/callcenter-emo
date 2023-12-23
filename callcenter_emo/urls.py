"""
URL configuration for callcenter_emo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.accounts.views import UserRoleViewSet, UserViewSet, LoginView


# 创建 apps 里应用的路由并注册
router = routers.DefaultRouter()
router.register('roles', UserRoleViewSet)  # 角色路由
router.register('users', UserViewSet)      # 用户路由

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger接口文档
    path('api-doc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # redoc接口文档
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取Token的接口
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新Token有效期的接口
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # 验证Token的有效性
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),  # apps 中应用的路由
]
