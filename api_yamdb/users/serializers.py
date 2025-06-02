from rest_framework import serializers
from django.core.validators import RegexValidator
from users.models import User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Недопустимые символы в username.'
            )
        ]
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать me как username.'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user = User.objects.filter(username=username).first()
        if user:
            if user.email != email:
                raise serializers.ValidationError({
                    'email': (
                        'Пользователь с таким username уже'
                        'зарегистрирован с другим email.'
                    )
                })
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )