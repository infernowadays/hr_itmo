from django.db import models

from token_auth.models import UserProfile


class TelegramBot(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=32, null=True, blank=False)

    class Meta:
        unique_together = ('user', 'chat_id',)
        db_table = 'telegram_bot'
