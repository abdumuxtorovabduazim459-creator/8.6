from rest_framework import serializers

from .models import Genre, Book, Comment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = []
        read_only_fields = ['id']
        extra_kwargs = {
            'pages': {'min_value': 1},
        }


class BookInGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['genre']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = []

    def get_genre(self, obj):
        if obj.genre is None:
            return None
        return {
            'id': obj.genre.id,
            'name': obj.genre.name,
            'description': obj.genre.description,
        }


class GenreSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(
        source='book_set', many=True, read_only=True, slug_field='title'
    )

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'min_length': 2},
            'description': {'required': False},
        }


class GenreDetailSerializer(GenreSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):
        books = obj.book_set.all()
        return BookInGenreSerializer(books, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
