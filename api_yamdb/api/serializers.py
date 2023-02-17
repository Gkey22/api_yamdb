from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField 
from reviews.models import Categorie, Genre, Title
from rest_framework.validators import UniqueTogetherValidator 

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User


class SerializerUser(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class SerializerUserRegistration(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        """Проверяет, не пытается ли юзер зарегистрироваться как 'me'."""
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Вы не можете зарегистрироваться с таким логином. Выберите другое имя.'
            )
        return data

    def create(self, validated_data):
        """Создает пользователя и отправляет код подтверждения почтой."""
        user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        self.send_notification(user)

        return user

    def send_notification(self, user):
        send_mail(
            'Подтверждение регистрации',
            f'{user.username}, Вы получили код подтверждения регистрации: {user.confirmation_code}.',
            'support@yamdb.com',
            [user.email],
            fail_silently=False,
        )


class MyTokenObtainPairSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        user = get_object_or_404(User, username=attrs[self.username_field])
        if authenticate_kwargs["confirmation_code"] != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        self.user = authenticate(**authenticate_kwargs)
        access = self.get_tokens_for_user(user)
        return access

    def get_tokens_for_user(cls, user):
        access = AccessToken.for_user(user)
        print(access)
        return {
            'access': str(access),
        }


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
