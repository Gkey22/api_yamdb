from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)


from .views import (CategorieViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet, signup_new_user,
                       get_token, UserViewSet
                       )


router = DefaultRouter()
router.register('users', UserViewSet)
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
    path('auth/token/', signup_new_user, name='token_obtain_pair'),
    path('token/refresh/', get_token, name='token_refresh'),
    path('v1/', include(router.urls)), 
    path('v1/', include('djoser.urls.jwt')),
]
