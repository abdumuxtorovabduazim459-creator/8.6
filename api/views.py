from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions

from .models import Genre, Book, Comment
from .serializers import (GenreSerializer, GenreDetailSerializer,
                          BookSerializer, BookDetailSerializer,
                          CommentSerializer)
from .permissions import IsCommentOwner


class GenreViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Genre.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GenreDetailSerializer
        return GenreSerializer


class BookViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
