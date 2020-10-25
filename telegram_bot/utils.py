import requests
from django.conf import settings
from django.db.utils import IntegrityError

from form.models import Form
from form.serializers import FormSerializer
from token_auth.models import UserProfile
from .models import TelegramBot
from .serializers import TelegramBotSerializer


class TelegramBotMixin:
    def __init__(self, specializations, vacancy_id):
        self.bot_url = 'https://api.telegram.org/bot' + settings.TELEGRAM_BOT_ACCESS_TOKEN
        self.link = 'http://findfound.me/vacancies?id=' + str(vacancy_id)
        self.specializations = specializations

    def get_updates(self):
        method = '/getUpdates'

        response = requests.get(self.bot_url + method)
        for update in response.json().get('result'):
            user = UserProfile.objects.filter(telegram=update.get('message').get('chat').get('username'))
            if user:
                serializer = TelegramBotSerializer(data={'chat_id': str(update.get('message').get('chat').get('id'))})
                if serializer.is_valid():
                    try:
                        serializer.save(user=user[0])
                    except IntegrityError:
                        pass

        self.compare_specializations()

    def compare_specializations(self):
        for telegram_object in TelegramBot.objects.all():
            form = Form.objects.filter(student=telegram_object.user)
            if form:
                educations = FormSerializer(instance=form[0]).data.get('educations')
                for education in educations:
                    if education.get('specialization').get('id') in self.specializations:
                        self.send_message(telegram_object.chat_id)

    def send_message(self, chat_id):
        method = '/sendMessage'
        payload = {'chat_id': chat_id, 'text': 'Ура! Новая вакансия по вашей специализации: ' + self.link}

        requests.get(self.bot_url + method, params=payload)
