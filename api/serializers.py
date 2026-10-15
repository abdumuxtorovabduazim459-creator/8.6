from rest_framework import serializers
from .models import Genre, Book, Comment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'          


class BookInGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['genre']        


class GenreShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_genre(self, obj):       
        if obj.genre:
            return GenreShortSerializer(obj.genre).data
        return None


class GenreSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(
        source='book_set', many=True, read_only=True, slug_field='title'
    )

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books']


class GenreDetailSerializer(GenreSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):      
        return BookInGenreSerializer(obj.book_set.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
