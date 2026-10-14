from rest_framework import serializers

from .models import Genre, Book, Comment


class BookSerializer(serializers.ModelSerializer):
    genre_info = serializers.SerializerMethodField()

    class Meta:
        model = Book
        exclude = []
        read_only_fields = ['id']
        extra_kwargs = {
            'pages': {'min_value': 1},
        }

    def get_genre_info(self, obj):
        if obj.genre is None:
            return None
        return {
            'id': obj.genre.id,
            'name': obj.genre.name,
            'description': obj.genre.description,
        }


class GenreSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'min_length': 2},
            'description': {'required': False},
        }

    def get_books(self, obj):
        books = obj.book_set.all()
        if self.context['view'].kwargs.get('pk'):
            return [
                {
                    'id': b.id,
                    'title': b.title,
                    'author': b.author,
                    'pages': b.pages,
                    'published_year': b.published_year,
                }
                for b in books
            ]
        return [b.title for b in books]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
