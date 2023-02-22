from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (CategorieViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet, signup_new_user,
                    get_token, UserViewSet
                    )


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
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
    path('v1/auth/signup/', signup_new_user, name='get_code'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
