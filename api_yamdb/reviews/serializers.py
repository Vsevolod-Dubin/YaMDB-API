# reviews/serializers.py

from rest_framework import serializers
from reviews.models import Review, Comment, Title


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = ['id', 'name', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ('title', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('pub_date', 'id', 'review')
