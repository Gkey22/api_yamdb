from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView

)
from .views import UserViewSet, UserRegistrationViewSet, ProfileViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('auth/signup', UserRegistrationViewSet)
router.register('users/me', ProfileViewSet)


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
