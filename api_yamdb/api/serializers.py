from rest_framework import serializers 
from rest_framework.relations import SlugRelatedField 
from reviews.models import Categorie, Genre, Title
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt


class CategorieSerializer(serializers.ModelSerializer): 
    slug = SlugRelatedField(slug_field='name', read_only=True) 
 
    class Meta: 
        fields = ('name', 'slug')
        model = Categorie
 
 
class GenreSerializer(serializers.ModelSerializer): 
    slug = SlugRelatedField(read_only=True, slug_field='name')
 
    class Meta: 
        fields = ('name', 'slug')
        model = Genre 
 
 
class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(required=False)
 
    class Meta: 
        fields = ('id', 'name', 'year', 'category', 'genre', 'rating', 'description')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not ( value > year):
            raise serializers.ValidationError('Произведение ещё не вышло!')
        return value