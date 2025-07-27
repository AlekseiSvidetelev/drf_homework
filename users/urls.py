from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet, UserCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes = (AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes = (AllowAny,)), name='token_refresh'),
]

urlpatterns += router.urls
