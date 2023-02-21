from rest_framework import serializers
from rest_framework.relations import SlugRelatedField 
import datetime as dt
from reviews.models import Categorie, Genre, Title, User, Comment, Review
from rest_framework.validators import UniqueTogetherValidator 

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


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
        user = User.objects.create(
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

    def get_tokens_for_user(self, user):
        access = AccessToken.for_user(user)
        print(access)
        return {
            'access': str(access),
        }


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
