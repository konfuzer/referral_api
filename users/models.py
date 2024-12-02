from django.db import models


class User(models.Model):
    """
    Модель пользователя.
    Содержит номер телефона, инвайт-код и активированный инвайт-код.
    """
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    invite_code = models.CharField(
        max_length=6, unique=True, blank=True, null=True)
    activated_invite_code = models.CharField(
        max_length=6, blank=True, null=True)

    def __str__(self):
        return self.phone_number


class Referral(models.Model):
    """
    Модель рефералов, связывающая пользователей с активированными инвайт-кодами.
    """
    user = models.ForeignKey(
        User, related_name='referrals', on_delete=models.CASCADE)
    invited_user = models.ForeignKey(
        User, related_name='invited_by', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.invited_user.phone_number} invited by {self.user.phone_number}"
