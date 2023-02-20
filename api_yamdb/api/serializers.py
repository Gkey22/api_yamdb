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
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    categorie = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(required=False)
 
    class Meta: 
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not ( value < year):
            raise serializers.ValidationError('Произведение ещё не вышло!')
        return value