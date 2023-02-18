from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import User

from reviews.models import Categorie, Genre, Title 
from rest_framework import viewsets, permissions, mixins, filters 
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination 
from .serializers import (CategorieSerializer, GenreSerializer, 
                          TitleSerializer, SerializerUser,
                          SerializerUserRegistration
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
