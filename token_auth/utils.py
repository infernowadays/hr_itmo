import datetime
import json
import secrets

import requests

from .enums import Sex


def get_json_user(json_user, email):
    user = dict({})
    user['email'] = email
    user['first_name'] = json_user.get('first_name')
    user['last_name'] = json_user.get('last_name')
    user['date_of_birth'] = get_date(json_user.get('bdate'))
    user['sex'] = get_sex(json_user.get('sex'))
    user['password'] = secrets.token_hex(nbytes=16)
    return user


def get_sex(sex):
    if sex == 0:
        return Sex.UNSURE.value
    elif sex == 1:
        return Sex.FEMALE.value
    elif sex == 2:
        return Sex.MALE.value


def get_date(date):
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')


def get_profile_info(access_token):
    payload = {
        'access_token': access_token,
        'v': '5.130',
    }

    app_url = 'https://api.vk.com/method/account.getProfileInfo'
    response = requests.get(app_url, params=payload)
    json_response = response.content.decode('utf8').replace("'", '"')
    return json.loads(json_response)
