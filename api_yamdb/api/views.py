from .serializers import (CommentSerializer,
                          ReviewSerializer)




class ReviewViewSet(viewsets.ModelViewSet):
    """Получение, создание, обновление, удаление отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)

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
    permission_classes = (IsAuthorOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
