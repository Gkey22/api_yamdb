from posts.models import Categorie, Genre, Title 
from rest_framework import viewsets, permissions, mixins, filters 
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination 
from .serializers import (CategorieSerializer, GenreSerializer, 
                          TitleSerializer 
                          ) 


class CategorieViewSet(viewsets.ModelViewSet): 
    queryset = Categorie.objects.all() 
    serializer_class = CategorieSerializer 
    pagination_class = LimitOffsetPagination 
 
    def perform_create(self, serializer): 
        serializer.save(author=self.request.admin) 
 
 
class GenreViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Genre.objects.all() 
    serializer_class = GenreSerializer 
    permission_classes = (permissions.IsAdminUser, )
    pagination_class = LimitOffsetPagination 
 
 
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer 
    pagination_class = LimitOffsetPagination
