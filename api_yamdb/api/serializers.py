from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from users.validators import validate_username

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = "__all__"
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all(),
        allow_null=False,
        allow_empty=False,
    )
    rating = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        fields = "__all__"
        model = Title

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]
        read_only_fields = ("title", "pub_date")

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        author = request.user

        if (
            request.method == "POST"
            and Review.objects.filter(
                title_id=title_id, author=author
            ).exists()
        ):
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ("review",)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username],
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    def validate(self, data):
        username = data['username']
        email = data['email']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            raise ValidationError({
                'email': (
                    'Пользователь с таким username уже '
                    'зарегистрирован с другим email.'
                )
            })

        if user_by_email and user_by_email.username != username:
            raise ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })

        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={'email': validated_data['email']}
        )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[validated_data['email']],
            fail_silently=False,
        )

        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail='Пользователь с таким username не найден.')

        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Неверный код подтверждения.')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError('Неверное значение роли')
        return value
