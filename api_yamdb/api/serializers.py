from rest_framework import serializers 
from rest_framework.relations import SlugRelatedField 
from posts.models import Categorie, Genre, Title
from rest_framework.validators import UniqueTogetherValidator 


class CategorieSerializer(serializers.ModelSerializer): 
    slug = SlugRelatedField(slug_field='name', read_only=True) 
 
    class Meta: 
        fields = '__all__' 
        model = Categorie
 
 
class GenreSerializer(serializers.ModelSerializer): 
    slug = SlugRelatedField(read_only=True, slug_field='name')
 
    class Meta: 
        fields = '__all__' 
        model = Genre 
 
 
class TitleSerializer(serializers.ModelSerializer): 
 
    class Meta: 
        fields = '__all__' 
        model = Title 
