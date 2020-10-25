from rest_framework.serializers import ModelSerializer

from token_auth.serializers import UserProfileSerializer
from .models import TelegramBot


class TelegramBotSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = TelegramBot
        fields = '__all__'
