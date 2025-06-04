from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .serializers import SignupSerializer, TokenSerializer, UserSerializer
from users.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Метод PUT не разрешён.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    permission_classes = []

    @action(methods=['post'], detail=False, url_path='signup')
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(username=username)
            if user.email != email:
                raise ValidationError(
                    {'email': 'Пользователь с таким username уже существует.'}
                )
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='yamdb@mail.ru',
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'email': email, 'username': username})


    @action(methods=['post'], detail=False, url_path='token')
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )

        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
