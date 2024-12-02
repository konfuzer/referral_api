from django.contrib import admin
from .models import User, Referral


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админка для модели User.
    """
    list_display = ('phone_number', 'invite_code', 'activated_invite_code')
    search_fields = ('phone_number',)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """
    Админка для модели Referral.
    """
    list_display = ('user',)
