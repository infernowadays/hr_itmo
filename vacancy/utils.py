from django.db.models import Q
from vacancy.models import Skill
from .constants import *
from core.models import Specialization
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
