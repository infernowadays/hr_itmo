import requests
from django.conf import settings
from django.db.models import Q

from company.models import Company
from core.models import Specialization, JobDuties, Duty
from vacancy.models import Skill
from vacancy.models import Vacancy, Job
from .constants import *
from .models import VacancySkills, VacancyJobs


def filter_by_request_types(list_roles, user):
    q = Q()
    if list_roles:
        for role in list_roles:
            if role == 'creator':
                companies_ids = Company.objects.filter(profile=user).values_list('id', flat=True).distinct()
                vacancies_ids = Vacancy.objects.filter(company_id__in=companies_ids).values_list('id',
                                                                                                 flat=True).distinct()
                q = q | Q(vacancy_id__in=vacancies_ids)
            elif role == 'member':
                q = q | Q(user=user)

    else:
        q = Q(~Q(creator=user) & ~Q(members=user))

    return q


def filter_by_skills(skill_text):
    if skill_text:
        skill = Skill.objects.filter(text__icontains=skill_text.lower()).values_list('id', flat=True)
        return Q(skills__in=skill)
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
        return Q(Q(name__icontains=text) | Q(description__icontains=text))
    else:
        return Q()


def filter_by_experience_type(experience_type):
    if experience_type:
        return Q(experience_type=experience_type)
    else:
        return Q()


def filter_by_type_of_work(type_of_work):
    if type_of_work:
        return Q(type_of_work=type_of_work)
    else:
        return Q()


def setup_vacancy_display(vacancies):
    for vacancy in vacancies:
        setup_single_vacancy_display(vacancy)

    return vacancies


def setup_single_vacancy_display(vacancy):
    vacancy['employment_type'] = {'id': vacancy.get('employment_type'),
                                  'text': Constants().get_employment_types(vacancy.get('employment_type'))}

    vacancy['experience_type'] = {'id': vacancy.get('experience_type'),
                                  'text': Constants().get_experience_types(vacancy.get('experience_type'))}

    vacancy['schedule_type'] = {'id': vacancy.get('schedule_type'),
                                'text': Constants().get_schedule_types(vacancy.get('schedule_type'))}

    return vacancy


def create_vacancy_skills(vacancy, skills):
    VacancySkills.objects.filter(vacancy_id=vacancy.id).delete()
    for string_skill in skills:
        skill = Skill.objects.filter(text=string_skill.get('text'))

        if not skill:
            skill = Skill.objects.create(text=string_skill.get('text'))
        else:
            skill = skill.get()

        VacancySkills.objects.create(vacancy=vacancy, skill=skill)


def create_vacancy_jobs(vacancy, jobs):
    VacancyJobs.objects.filter(vacancy_id=vacancy.id).delete()
    for job in jobs:
        duties = job.pop('duties')
        job = Job.objects.create(**job)
        for duty in duties:
            duty = Duty.objects.create(text=duty)
            JobDuties.objects.create(job=job, duty=duty)
        VacancyJobs.objects.create(vacancy=vacancy, job=job)


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
               'count': count, 'keywords': keywords, 'type_of_work': type_of_work, 'experience': experience, }

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
