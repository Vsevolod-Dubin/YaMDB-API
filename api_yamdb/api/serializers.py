from rest_framework import serializers
from works.models import Title, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'category', 'genres']
