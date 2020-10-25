import requests
from django.conf import settings
from django.db.models import Q

from company.models import Company
from core.models import Specialization
from vacancy.models import Skill
from vacancy.models import Vacancy
from .constants import *
from .models import VacancySkills


def filter_by_skills(list_skills):
    if list_skills:
        skills = Skill.objects.filter(id__in=list_skills).values_list('id', flat=True)
        return Q(skills__in=skills)
    else:
        return Q()


def filter_by_specializations(list_specializations):
    if list_specializations:
        specializations = Specialization.objects.filter(id__in=list_specializations).values_list('id', flat=True)
        return Q(specializations__in=specializations)
    else:
        return Q()


def filter_by_text(text):
    if text:
        return Q(Q(name__icontains=text) | Q(short_description__icontains=text) | Q(description__icontains=text))
    else:
        return Q()


def setup_vacancy_display(vacancies):
    for vacancy in vacancies:
        vacancy['experience_type'] = {'id': vacancy.get('experience_type'),
                                      'text': Constants().get_employment_types(vacancy.get('experience_type'))}

        vacancy['employment_type'] = {'id': vacancy.get('employment_type'),
                                      'text': Constants().get_experience_types(vacancy.get('employment_type'))}

        vacancy['schedule_type'] = {'id': vacancy.get('schedule_type'),
                                    'text': Constants().get_schedule_types(vacancy.get('schedule_type'))}


def create_skills(skills, vacancy):
    for string_skill in skills:
        skill = Skill.objects.filter(text=string_skill.get('text'))

        if not skill:
            skill = Skill.objects.create(id=string_skill.get('id'), text=string_skill.get('text'))
        else:
            skill = skill.get()

        VacancySkills.objects.create(vacancy=vacancy, skill=skill)


class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self


def get_super_job_vacancies(keywords, type_of_work, experience):
    app_url = 'https://api.superjob.ru/2.20/vacancies/'
    period = 0
    town = 'Ставрополь'
    order_field = 'date'
    order_direction = 'desc'
    count = 10

    # , 'type_of_work': type_of_work, 'experience': experience
    headers = {'Content-Type': 'application/json', 'X-Api-App-Id': settings.SUPER_JOB_SECRET_KEY}
    payload = {'period': period, 'town': town, 'order_field': order_field, 'order_direction': order_direction,
               'count': count, 'keywords': keywords}

    response = requests.get(app_url, headers=headers, params=payload)
    vacancies = list([])
    for vacancy_json in response.json().get('objects'):
        vacancy = dict({})

        vacancy['id'] = 1000

        vacancy['name'] = vacancy_json.get('profession')
        vacancy['short_description'] = vacancy_json.get('candidat')
        vacancy['description'] = vacancy_json.get('candidat')
        vacancy['salary'] = vacancy_json.get('payment_from')
        vacancy['experience_type'] = vacancy_json.get('experience').get('id')

        if vacancy_json.get('type_of_work').get('id') == 6:
            vacancy['schedule_type'] = 1
        elif vacancy_json.get('type_of_work').get('id') == 10:
            vacancy['schedule_type'] = 2
        elif vacancy_json.get('type_of_work').get('id') == 7:
            vacancy['schedule_type'] = 3

        vacancy['employment_type'] = 1

        vacancy['external'] = True
        vacancy['link'] = vacancy_json.get('link')

        company_json = {'name': vacancy_json.get('firm_name')}
        company = Company(**company_json)
        vacancy['company'] = company

        instance = Vacancy(**vacancy)
        vacancies.append(instance)

    return vacancies
