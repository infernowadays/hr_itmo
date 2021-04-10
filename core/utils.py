import json

import requests


def handle_serializer_errors(model, errors):
    error_message = "Поля, обязательные для заполнения: "
    empty = True
    for error in errors:
        for field in model._meta.fields:
            if error == field.attname:
                if empty is False:
                    error_message += ", "
                error_message += errors.get(field.attname)[0]
                empty = False
    return error_message


def get_hh_skills(text):
    app_url = 'https://api.hh.ru/suggests/skill_set?text=' + str(text)
    response = requests.get(app_url)
    json_response = response.content.decode('utf8').replace("'", '"')
    items = json.loads(json_response).get('items')
    if items is not None and len(items) > 0:
        return items[0].get('text')
    return ''
