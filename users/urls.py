from django.urls import path
from .views import UserLoginView, UserActivateInviteCodeView, UserProfileView, home, login_view, profile_view


urlpatterns = [
    path('login/', UserLoginView.as_view(),
         name='user_login'),  # Логин пользователя
    path('activate-invite-code/', UserActivateInviteCodeView.as_view(),
         name='activate_invite_code'),  # Активация инвайт-кода
    path('profile/', UserProfileView.as_view(),
         name='user_profile'),  # Профиль пользователя
    path('login-page/', login_view, name='login_page'),  # Страница логина
    path('profile-page/', profile_view, name='profile_page'),
    path('', home, name='home'),
]
