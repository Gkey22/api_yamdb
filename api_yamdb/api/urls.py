from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

from .views import UserViewSet, UserRegistrationViewSet, ProfileViewSet
from api.views import (CategorieViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet
                       )


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('auth/signup', UserRegistrationViewSet)
router.register('users/me', ProfileViewSet)
router.register(r'categories', CategorieViewSet, basename='categorys')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews'
                )
router.register(r'titles/(?P<title_id>\d+)/reviews/('
                r'?P<review_id>\d+)/comments', CommentViewSet,
                basename='comments'
                )                


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)), 
    path('v1/', include('djoser.urls.jwt')),
]
