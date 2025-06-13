import re
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from users.constants import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Недопустимые символы в username.',
            )
        ],
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Имя пользователя "me" запрещено.')

        invalid_chars = re.sub(r'[\w.@+-]', '', value)
        if invalid_chars:
            raise ValidationError(
                f'Недопустимые символы:{", ".join(sorted(set(invalid_chars)))}'
            )
        return value

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
            from_email='yamdb@mail.ru',
            recipient_list=[validated_data['email']],
            fail_silently=False,
        )

        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default=User.USER
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError('Неверное значение роли')
        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and not request.user.is_admin:
            validated_data.pop('role', None)
        return super().update(instance, validated_data)
