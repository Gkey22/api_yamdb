from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import CategorieViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
 
urlpatterns = [ 
    path('v1/', include(router.urls)), 
    path('v1/', include('djoser.urls.jwt')),
]