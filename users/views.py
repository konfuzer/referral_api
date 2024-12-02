import time
import random
import string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import render
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, ActivateInviteCodeSerializer


def generate_invite_code():
    """
    Генерация случайного 6-значного инвайт-кода.
    Код состоит из цифр и букв.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def send_code(request, phone_number):
    """
    Имитация отправки кода на телефон.
    Сохраняем код в сессии.
    """
    code = str(random.randint(1000, 9999))  # Генерация 4-значного кода
    request.session['auth_code'] = code  # Сохраняем код в сессии
    print(f"Код {code} отправлен на номер {phone_number}")  # Имитация отправки


class VerifyCodeView(APIView):
    """
    Представление для проверки кода авторизации.
    """

    def post(self, request):
        code = request.data.get('code')
        if code == request.session.get('auth_code'):
            phone_number = request.session.get('phone_number')
            user, created = User.objects.get_or_create(
                phone_number=phone_number)
            return Response({'message': 'Вы успешно авторизованы.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    Представление для авторизации пользователя по номеру телефона.
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            # Имитируем задержку на сервере
            time.sleep(2)
            user, created = User.objects.get_or_create(
                phone_number=phone_number)
            if created:
                user.invite_code = generate_invite_code()
                user.save()
            return Response({'message': 'Код отправлен на телефон.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivateInviteCodeView(APIView):
    """
    Представление для активации инвайт-кода.
    """

    def post(self, request):
        serializer = ActivateInviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            user = request.user  # Предполагаем, что пользователь аутентифицирован
            if user.activated_invite_code:
                return Response({'message': 'Вы уже активировали инвайт-код.'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(invite_code=invite_code).exists():
                user.activated_invite_code = invite_code
                user.save()
                return Response({'message': 'Инвайт-код активирован.'}, status=status.HTTP_200_OK)
            return Response({'message': 'Инвайт-код не существует.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Представление для получения профиля пользователя.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user  # Предполагаем, что пользователь аутентифицирован
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def login_view(request):
    """
    Представление для отображения страницы логина.
    """
    return render(request, 'login.html')


def profile_view(request):
    """
    Представление для отображения профиля пользователя.
    """
    return render(request, 'profile.html')


def home(request):
    """
    Представление для отображения домашней страницы.
    """
    return render(request, 'home.html')
