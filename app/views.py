import json
import random
from functools import wraps
from json.decoder import JSONDecodeError

import bcrypt
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from app.models import *

TERMS = {
    1: 'Без зарплаты',
    2: 'С зарплатой',
    3: 'Доля компании'
}
OCCUPATION = {
    1: '10 часов в неделю',
    2: '20 часов в неделю',
    3: '30 часов в неделю',
    4: '40 часов в неделю',
}
WORK_FORMAT = {
    1: 'Личное присутствие',
    2: 'Удаленная работа'
}
ROLES = {
    1: 'Участник',
    42: 'Компания'
}


def auth_user(group=None):
    if group is None:
        group = 1

    def decorator(function, *args, **kwargs):
        @wraps(function)
        def inner(request, *args, **kwargs):
            if 'X-JWT' not in request.headers:
                return Response({'status': 'error', 'message': 'Отказано в доступе', "action": "reject1"}, 400)
            try:
                payload = jwt.decode(request.headers['X-JWT'], settings.SECRET_KEY)
                user = User.objects.get(pk=payload['user_id'])
                if user:
                    if user.role >= group:
                        return function(request, user, *args, **kwargs)
                    else:
                        return Response({"status": "error", "message": "Недостаточно прав"}, 400)
                else:
                    return Response({"status": "error", "message": "Отказано в доступе"}, 400)
            except jwt.DecodeError or jwt.ExpiredSignatureError or jwt.InvalidTokenError:
                return Response({"status": "error", "message": "Отказано в доступе", "action": "reject2"}, 400)
            except User.DoesNotExist:
                return Response({"status": "error", "message": "Отказано в доступе", "action": "reject3"}, 400)

        return inner

    return decorator


def Response(result=None, code=200):
    if result is None:
        result = {"status": "success"}

    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False}, status=code)


@csrf_exempt
@require_http_methods(['POST'])
def registration(request):
    data = json.loads(request.body)
    if 'login' not in data:
        return Response({"status": "error", "message": "Не отправлен логин"}, 400)
    if 'password' not in data:
        return Response({"status": "error", "message": "Не отправлен пароль"}, 400)
    if 'surname' not in data:
        return Response({"status": "error", "message": "Не отправлена фамилия"}, 400)
    if 'name' not in data:
        return Response({"status": "error", "message": "Не отправлено имя"}, 400)
    if 'patronymic' not in data:
        return Response({"status": "error", "message": "Не отправлено отчество"}, 400)
    if 'email' not in data:
        return Response({"status": "error", "message": "Не отправлен почта"}, 400)
    if 'phone' not in data:
        return Response({"status": "error", "message": "Не отправлен телефон"}, 400)
    password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
    if User.objects.filter(login=data['login']).exists():
        return Response({"status": "error", "message": "Такой логин уже существует"}, 400)
    if User.objects.filter(email=data['email']).exists():
        return Response({"status": "error", "message": "Такая почта уже существует"}, 400)
    try:
        user = User.objects.create(
            login=data['login'],
            email=data['email'],
            password=password.decode('utf-8'),
            name=data['name'],
            surname=data['surname'],
            patronymic=data['patronymic'],
            phone=data['phone'],
            role=1)
    except IntegrityError as e:
        user.delete()
        return Response({"status": "error", "message": f"Ошибка при регистрации {e}"}, 400)
    except Exception as e:
        if e.args[0] == 1406:
            user.delete()
            return Response({"status": "error", "message": "Слишком длинный номер телефона"}, 400)
        else:
            user.delete()
            print(e)
            return Response({"status": "error", "message": "Возникла ошибка. Повторите снова"}, 400)
    return Response()


@csrf_exempt
@require_http_methods(['POST'])
def auth(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return Response({"status": "error", "message": "Неверный JSON"}, 400)
    if 'login' not in data:
        return Response({'status': "error", "message": "Отсутствует логин"}, 400)

    if 'password' not in data:
        return Response({'status': "error", "message": "Отсутствует пароль"}, 400)
    try:
        user = User.objects.get(login=data['login'])
    except ObjectDoesNotExist:
        return Response({"status": "error", "message": "Неправильный логин или пароль"}, 400)
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return Response({"status": "error", "message": "Неправильный логин или пароль"}, 400)
    access_token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm='HS256')
    return Response({"status": "success", "token": access_token.decode('utf-8'), "role": ROLES[user.role]})


def getFullCompany(company):
    return {
        "id": company.id,
        "name": company.name,
        "short_name": company.short_name,
        "logo": settings.HOST + company.logo.file.url if company.logo is not None else '',
        "description": company.description,
        "departments": [getFullDepartment(item) for item in company.departments.all()]
    }


def getShortCompany(company):
    return {
        "id": company.id,
        "name": company.name,
        "short_name": company.short_name,
        "logo": settings.HOST + company.logo.file.url if company.logo is not None else '',
        "description": company.description
    }


def getShortDepartment(department):
    return {
        "id": department.id,
        "name": department.name,
        "company": getShortCompany(department.company_set.first())
    }


def getFullDepartment(dep):
    return {
        "id": dep.id,
        "name": dep.name,
        "company": getShortCompany(dep.company_set.first()),
        "projects": [getProject(item) for item in dep.projects.all()]
    }


def getProject(item):
    return {
        "id": item.id,
        "name": item.name,
        "description": item.name,
        "department": getShortDepartment(item.department_set.first())
    }


def getParticipant(item):
    return {
        "id": item.id,
        "name": item.name,
        "surname": item.surname,
        "patronymic": item.patronymic,
        "avatar": settings.HOST + item.avatar.file.url if item.avatar is not None else '',
        "description": item.description,
        "technologies": item.technologies
    }


def getVacancy(item):
    return {
        "id": item.id,
        "name": item.name,
        "participants": [getParticipant(participant) for participant in item.participants.all()],
        "terms": TERMS[item.terms],
        "occupation": OCCUPATION[item.occupation],
        "work_format": WORK_FORMAT[item.work_format],
        "project": getProject(item.project_set.first())
    }


@auth_user(1)
@csrf_exempt
@require_http_methods(['POST', 'GET'])
def projects(request, user):
    if request.method == 'GET':
        data = request.GET.copy()
        if "department_id" in data:
            project_instance = Project.objects.filter(department__id=data['department_id']).first()
            if project_instance is not None:
                return Response(getProject(project_instance))
            else:
                return Response([])
        if 'id' not in data:
            if 'count' not in data:
                return Response({"status": "error", "message": "Не отправлено количество проектов"}, 400)
            elif 'count' in data:
                if data['count'] == '':
                    count = 10
                try:
                    count = int(data['count'])
                except ValueError:
                    return Response({"status": "error", "message": "Неверный формат количества"}, 400)
                ids_projects = list(Project.objects.values_list('id', flat=True))
                rand_ids = random.sample(ids_projects, min(len(ids_projects), count))
                rand_projects = Project.objects.filter(id__in=rand_ids)
                return Response([getProject(item) for item in rand_projects])
        else:
            project_instance = Project.objects.filter(id=data['id']).first()
            if project_instance is not None:
                return Response(getProject(project_instance))
            else:
                return Response({})
    elif request.method == 'POST':
        if user.role < 42:
            return Response({"status": "error", "message": "Запрещено"}, 400)
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return Response({"status": "error", "message": "Неверный JSON"}, 400)
        if 'action' not in data:
            return Response({"status": "error", "message": "Не указано действие"}, 400)
        if data['action'] == 'create':
            if 'name' not in data:
                return Response({"status": "error", "message": "Нет названия"}, 400)
            if 'description' not in data:
                return Response({"status": "error", "message": "Нет описания"}, 400)
            if 'department_id' not in data:
                return Response({"status": "error", "message": "Нет департамента"}, 400)
            department_instance = Department.objects.filter(id=data["department_id"]).first()
            if department_instance is not None:
                company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
                if department_instance in company_instance.departments.all():
                    project_instance = Project.objects.create(name=data['name'], description=data['description'])
                    department_instance.projects.add(project_instance)
                    return Response({"status": "success", 'payload': getProject(project_instance)})
                else:
                    return Response({"status": "error", "message": "Недостаточно прав"}, 400)
            else:
                return Response({"status": "error", "message": "Недостаточно прав"}, 400)
        elif data['action'] == 'delete':
            if 'id' in data:

                project_instance = Project.objects.filter(id=data['id']).first()
                if project_instance is not None:
                    department_instances = Department.objects.filter(company__id=user.affiliated_company.id).all()
                    for department_instance in department_instances:
                        if project_instance in department_instance.projects.all():
                            project_instance.delete()
                            return Response()
                    else:
                        return Response({"status": "error", "message": "Недостаточно прав"}, 400)
                else:
                    return Response({"status": "error", "message": "Нет такого проекта"}, 400)
            else:
                return Response({"status": "error", "message": "Нет id"}, 400)


@auth_user(1)
@csrf_exempt
@require_http_methods(['POST', 'GET'])
def departments(request, user):
    if request.method == 'GET':
        data = request.GET.copy()
        if 'id' not in data:
            department_instances = user.affiliated_company.departments.all()
            return Response([getFullDepartment(item) for item in department_instances])
        else:
            department_instance = Department.objects.filter(id=data['id']).first()
            if department_instance is not None:
                return Response(getFullDepartment(department_instance))
            else:
                return Response({})
    elif request.method == 'POST':
        if user.role < 42:
            return Response({"status": "error", "message": "Запрещено"}, 400)
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return Response({"status": "error", "message": "Неверный JSON"}, 400)
        if 'action' not in data:
            return Response({"status": "error", "message": "Не указано действие"}, 400)
        if data['action'] == 'create':
            if 'name' not in data:
                return Response({"status": "error", "message": "Нет названия"}, 400)
            company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
            department_instance = Department.objects.create(name=data['name'])
            company_instance.departments.add(department_instance)
            return Response({"status": "success", 'payload': getShortDepartment(department_instance)})
        elif data['action'] == 'delete':
            if 'id' in data:
                company_instance = Company.objects.filter(id=user.affiliated_company.id).first()

                department_instance = Department.objects.filter(id=data['id']).first()
                if department_instance is not None:
                    if department_instance in company_instance.departments.all():
                        department_instance.delete()
                        return Response()
                    else:
                        return Response({"status": "error", "message": "Недостаточно прав"}, 400)
                else:
                    return Response({"status": "error", "message": "Нет такого департамента"}, 400)
            else:
                return Response({"status": "error", "message": "Нет id"}, 400)


@auth_user(1)
@csrf_exempt
@require_http_methods(['POST', 'GET'])
def vacancies(request, user):
    if request.method == 'GET':
        data = request.GET.copy()
        if 'project_id' in data:
            vacancy_instances = Vacancy.objects.filter(project__id=data['project_id'])
            return Response([getVacancy(item) for item in vacancy_instances])
        if 'search' in data:
            vacancy_instances = Vacancy.objects.filter(
                Q(name__icontains=data['search']) | Q(description__icontains=data['search']))
            return Response([getVacancy(item) for item in vacancy_instances])
        if 'id' not in data:
            if 'count' not in data:
                return Response({"status": "error", "message": "Не отправлено количество проектов"}, 400)
            elif 'count' in data:
                if data['count'] == '':
                    count = 10
                try:
                    count = int(data['count'])
                except ValueError:
                    return Response({"status": "error", "message": "Неверный формат количества"}, 400)
                ids_vacancies = list(Vacancy.objects.values_list('id', flat=True))
                rand_ids = random.sample(ids_vacancies, min(len(ids_vacancies), count))
                rand_vacancies = Vacancy.objects.filter(id__in=rand_ids)
                return Response([getVacancy(item) for item in rand_vacancies])
        else:
            vacancy_instance = Vacancy.objects.filter(id=data['id']).first()
            if vacancy_instance is not None:
                return Response(getVacancy(vacancy_instance))
            else:
                return Response({})
    elif request.method == 'POST':
        if user.role < 42:
            return Response({"status": "error", "message": "Запрещено"}, 400)
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return Response({"status": "error", "message": "Неверный JSON"}, 400)
        if 'action' not in data:
            return Response({"status": "error", "message": "Не указано действие"}, 400)
        if data['action'] == 'create':
            if 'name' not in data:
                return Response({"status": "error", "message": "Нет названия"}, 400)
            if 'participants' not in data:
                return Response({"status": "error", "message": "Нет участников"}, 400)
            if 'description' not in data:
                return Response({"status": "error", "message": "Нет описания"}, 400)
            if 'terms' not in data:
                return Response({"status": "error", "message": "Нет условий"}, 400)
            if 'occupation' not in data:
                return Response({"status": "error", "message": "Нет занятости"}, 400)
            if 'work_format' not in data:
                return Response({"status": "error", "message": "Нет формата работы"}, 400)
            if 'project_id' not in data:
                return Response({"status": "error", "message": "Нет проекта"}, 400)

            project_instance = Project.objects.filter(id=data['project_id']).first()
            company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
            if project_instance.department_set.first() not in company_instance.departments.all():
                return Response({"status": "error", "message": "Недостаточно прав"}, 400)
            vacancy_instance = Vacancy.objects.create(
                name=data['name'],
                description=data['description'],
                terms=data['terms'],
                occupation=data['occupation'],
                work_format=data['work_format']
            )
            for participant in data['participants']:
                vacancy_instance.participants.add(participant)
            project_instance.vacancies.add(vacancy_instance)
            vacancy_instance.refresh_from_db()
            return Response({"status": "success", 'payload': getVacancy(vacancy_instance)})
        elif data['action'] == 'delete':
            if 'id' in data:

                vacancy_instance = Vacancy.objects.filter(id=data['id']).first()
                if vacancy_instance is not None:
                    project_instance = vacancy_instance.project_set.first()
                    company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
                    if project_instance.department_set.first() not in company_instance.departments.all():
                        return Response({"status": "error", "message": "Недостаточно прав"}, 400)
                    else:
                        vacancy_instance.delete()
                        return Response()
                else:
                    return Response({"status": "error", "message": "Нет такой вакансии"}, 400)
            else:
                return Response({"status": "error", "message": "Нет id"}, 400)


@auth_user(1)
@csrf_exempt
@require_http_methods(['POST', 'GET'])
def participants(request, user):
    if request.method == 'GET':
        data = request.GET.copy()
        if 'id' not in data:
            participants_list = Participant.objects.filter(company=user.affiliated_company)
            return Response([getParticipant(item) for item in participants_list])
        else:
            participant_instance = Participant.objects.filter(id=data['id']).first()
            if participant_instance is not None:
                return Response(getParticipant(participant_instance))
            else:
                return Response({})
    elif request.method == 'POST':
        if user.role < 42:
            return Response({"status": "error", "message": "Запрещено"}, 400)
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return Response({"status": "error", "message": "Неверный JSON"}, 400)
        if 'action' not in data:
            return Response({"status": "error", "message": "Не указано действие"}, 400)
        if data['action'] == 'create':
            if 'name' not in data:
                return Response({"status": "error", "message": "Нет названия"}, 400)
            if 'surname' not in data:
                return Response({"status": "error", "message": "Нет участников"}, 400)

            participant_instance = Participant.objects.create(name=data['name'], surname=data['surname'])
            if 'patronymic' in data:
                participant_instance.patronymic = data['patronymic']
            if 'avatar' in data:
                file = File.objects.filter(name__icontains=data['avatar'].split("/")[-1]).first()
                participant_instance.avatar = file
            if 'description' in data:
                participant_instance.description = data['description']
            if 'technologies' in data:
                participant_instance.technologies = data['technologies']
            participant_instance.save()
            company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
            company_instance.participants.add(participant_instance)
            return Response({"status": "success", 'payload': getParticipant(participant_instance)})
        elif data['action'] == 'delete':
            if 'id' in data:
                participant_instance = Participant.objects.filter(id=data['id']).first()
                if participant_instance is not None:
                    company_instance = Company.objects.filter(id=user.affiliated_company.id).first()
                    if participant_instance not in company_instance.participants.all():
                        return Response({"status": "error", "message": "Недостаточно прав"}, 400)
                    else:
                        participant_instance.delete()
                        return Response()
                else:
                    return Response({"status": "error", "message": "Нет такой вакансии"}, 400)
            else:
                return Response({"status": "error", "message": "Нет id"}, 400)


@csrf_exempt
@auth_user(1)
@require_http_methods(['POST'])
def upload_photo(request, user):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            photo = File.objects.create(file=request.FILES['file'])
            photo.name = photo.file.name
            photo.save()
            return Response({"status": "success", "url": settings.HOST + photo.url})
        else:
            return Response({"status": "error", "message": f"Ошибка с сохранением фото {form.errors}"})


@csrf_exempt
@auth_user(1)
@require_http_methods(['GET'])
def companies(request, user):
    data = request.GET.copy()
    if 'id' not in data:
        companies_list = Company.objects.all()
        return Response([getFullCompany(item) for item in companies_list])
    else:
        company_instance = Company.objects.filter(id=data['id']).first()
        if company_instance is not None:
            return Response(getFullCompany(company_instance))
        else:
            return Response({})


@csrf_exempt
@auth_user(1)
@require_http_methods(['GET'])
def profile(request, user):
    return Response({
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "avatar": settings.HOST + user.avatar.file.url if user.avatar is not None else '',
        "experience": user.experience,
        "tags": [{"id": item.id, "name": item.title} for item in user.tags.all()],
        "terms": TERMS[user.terms],
        "occupation": OCCUPATION[user.occupation],
        "work_format": WORK_FORMAT[user.work_format],
        "email": user.email,
        "phone": user.phone,
        "affilated_company": getShortCompany(user.affiliated_company)
    })
