from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import  Comment, Review

User = get_user_model()



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
