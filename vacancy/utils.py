from django.db.models import Q
from vacancy.models import Skill
from .constants import *


def filter_by_skills(list_skills):
    if list_skills:
        skills = Skill.objects.filter(id__in=list_skills).values_list('id', flat=True)
        return Q(skills__in=skills)
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
