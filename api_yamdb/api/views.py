from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
import csv
from works.models import Title, Category, Genre
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


def load_csv_data(file_path, model_class, serializer_class):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    obj, created = model_class.objects.update_or_create(
                        slug=row['slug'],
                        defaults=dict(row)
                    )
                except ValidationError as e:
                    print(f"Ошибка при загрузке данных: {e}")
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        file_path = 'api_yamdb/static/data/categories.csv'
        load_csv_data(file_path, Category, CategorySerializer)
        return Response({'status': 'Данные успешно импортированы'})


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        file_path = 'api_yamdb/static/data/genres.csv'
        load_csv_data(file_path, Genre, GenreSerializer)
        return Response({'status': 'Данные успешно импортированы'})


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def genres(self, request, pk=None):
        title = get_object_or_404(Title, pk=pk)
        genre_ids = request.data.get('genres', [])
        title.genres.set(genre_ids)
        return Response(GenreSerializer(title.genres.all(), many=True).data)

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        file_path = 'api_yamdb/static/data/titles.csv'
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = Title.objects.create(
                        name=row['name'],
                        year=int(row['year']),
                        category=Category.objects.get(slug=row['category']),
                        description=row['description']
                    )
                    genre_slugs = row['genre'].split(',')
                    for slug in genre_slugs:
                        genre = Genre.objects.get(slug=slug)
                        title.genres.add(genre)
            return Response({'status': 'Данные успешно импортированы'}, status=201)
        except FileNotFoundError:
            return Response({'error': 'Файл не найден'}, status=404)
        except Exception as e:
            return Response({'error': f'Произошла ошибка: {str(e)}'}, status=500)
