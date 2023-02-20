from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categorys')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)), 
    path('v1/', include('djoser.urls.jwt')),
]
