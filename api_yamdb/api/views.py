from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import User

from reviews.models import Categorie, Genre, Title 
from rest_framework import viewsets, permissions, mixins, filters 
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination 
from .serializers import (CategorieSerializer, GenreSerializer, 
                          TitleSerializer, SerializerUser,
                          SerializerUserRegistration,
                          CommentSerializer, ReviewSerializer
                          )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUser
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUserRegistration
    queryset = User.objects.all()
    #permission_classes = [permissions.AllowAny,]
    #lookup_field = settings.USER_ID_FIELD


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUser
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)
        

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

 
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAdminUser, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение, создание, обновление, удаление отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение, создание, обновление, удаление комментария."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
