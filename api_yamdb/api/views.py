from api.mail_util import generate_and_send_confirmation_code_to_email
from reviews.models import Categorie, Genre, Title, Review, User
from rest_framework import viewsets, filters, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permission import (AdminOrReadOnly, IsAdminOrStaffPermission,
                          IsAuthorOrModerPermission, IsUserForSelfPermission
                          )
from .serializers import (CategorieSerializer, GenreSerializer, 
                          TitleSerializer, UserSerializer,
                          AuthSignUpSerializer,AuthTokenSerializer,
                          CommentSerializer, ReviewSerializer
                          )   


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrStaffPermission,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsUserForSelfPermission,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_new_user(request):
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['username'] != 'me':
            serializer.save()
            generate_and_send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Username указан невено!', status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = AuthSignUpSerializer(
        user, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        generate_and_send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Почта указана неверно!', status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token_data = {'token': str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        'Код подтверждения неверный', status=status.HTTP_400_BAD_REQUEST
    )


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = (AdminOrReadOnly,  )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )

 
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,  )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('categorie', 'genre', 'name', 'year')



class ReviewViewSet(viewsets.ModelViewSet):
    """Получение, создание, обновление, удаление отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsAuthorOrModerPermission)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение, создание, обновление, удаление комментария."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsAuthorOrModerPermission)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
