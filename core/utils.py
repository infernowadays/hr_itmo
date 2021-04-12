import json

import requests

from company.models import Category
from core.models import City


def handle_serializer_errors(model, errors):
    error_message = "Поля, обязательные для заполнения: "
    empty = True
    for error in errors:
        for field in model._meta.fields:
            if field.attname == 'category_id':
                field.attname = 'category'
            if error == field.attname:
                if empty is False:
                    error_message += ", "
                if field.attname == 'category':
                    error_message += 'отрасль'
                else:
                    error_message += errors.get(field.attname)[0]
                empty = False
    return error_message


def get_hh_skills(text):
    app_url = 'https://api.hh.ru/suggests/skill_set?text=' + str(text)
    response = requests.get(app_url)
    json_response = response.content.decode('utf8').replace("'", '"')
    items = json.loads(json_response).get('items')
    if items is not None and len(items) > 0:
        return [x['text'] for x in items][:10]
    return []


def get_city(city_request):
    if city_request:
        city = City.objects.filter(id=city_request)
        if len(city) > 0:
            return city[0]
        else:
            return None


def get_category(category_request):
    if category_request:
        category = Category.objects.filter(name=category_request)
        if len(category) > 0:
            return category[0]
        else:
            return Category.objects.create(name=category_request)
