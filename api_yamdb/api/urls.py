from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet,
                    ReviewViewSet)

app_name = 'api'

v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/('
                   r'?P<review_id>\d+)/comments', CommentViewSet,
                   basename='comments')
