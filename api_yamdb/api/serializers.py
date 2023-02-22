from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.mail import send_mail
from rest_framework.relations import SlugRelatedField 
import datetime as dt
from reviews.models import Categorie, Genre, Title, User, Comment, Review
from rest_framework.validators import UniqueTogetherValidator 

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username не корректный!')
        return data


class AuthSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)


class CategorieSerializer(serializers.ModelSerializer): 
 
    class Meta: 
        fields = ('name', 'slug')
        model = Categorie
 
 
class GenreSerializer(serializers.ModelSerializer): 
 
    class Meta: 
        fields = ('name', 'slug')
        model = Genre 
 
 
class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    categorie = CategorieSerializer()
    rating = serializers.IntegerField(required=False)
 
    class Meta: 
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'categorie')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not ( value < year):
            raise serializers.ValidationError('Произведение ещё не вышло!')
        return value
        

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title__id=title_id,
                                     author=author).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение')
        return data

    def validate_integer_number(self, score):
        if score > 10 or score < 1:
            raise serializers.ValidationError(
                'Выберете оценку от 1 до 10')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
