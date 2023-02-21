from rest_framework import serializers
from rest_framework.relations import SlugRelatedField 
import datetime as dt
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer): 
    # slug = SlugRelatedField(slug_field='name', read_only=True) 
 
    class Meta: 
        fields = ('name', 'slug')
        model = Category
 
 
class GenreSerializer(serializers.ModelSerializer): 
    # slug = SlugRelatedField(read_only=True, slug_field='name')
 
    class Meta: 
        fields = ('name', 'slug')
        model = Genre 
 
 
class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    categorie = CategorySerializer()
    rating = serializers.IntegerField(required=False)
 
    class Meta: 
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'categorie')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not ( value < year):
            raise serializers.ValidationError('Произведение ещё не вышло!')
        return value