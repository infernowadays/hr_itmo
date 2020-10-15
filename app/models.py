from django.db import models
from django.forms import ModelForm

TERMS = (
    (1, 'Без зарплаты'),
    (2, 'С зарплатой'),
    (3, 'Доля компании')
)
OCCUPATION = (
    (1, '10 часов в неделю'),
    (2, '20 часов в неделю'),
    (3, '30 часов в неделю'),
    (4, '40 часов в неделю'),
)
WORK_FORMAT = (
    (1, 'Личное присутствие'),
    (2, 'Удаленная работа')
)
ROLES = (
    (1, 'Участник'),
    (42, 'Компания')
)


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")
    avatar = models.ForeignKey("File", on_delete=models.CASCADE, null=True, blank=True)
    login = models.CharField(max_length=100, verbose_name="Логин")
    password = models.CharField(max_length=200, verbose_name="Пароль")
    experience = models.TextField(null=True, blank=True, verbose_name="Опыт работы")
    tags = models.ManyToManyField(to="Tag", verbose_name="Тэги")
    terms = models.IntegerField(default=1, choices=TERMS, verbose_name="Условия участия")
    occupation = models.IntegerField(default=1, choices=OCCUPATION, verbose_name="Занятость")
    work_format = models.IntegerField(default=1, choices=WORK_FORMAT, verbose_name="Формат работы")
    email = models.EmailField(null=True, blank=True, verbose_name="Емейл")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Телефон")
    role = models.IntegerField(default=1, choices=ROLES, blank=True, null=True, verbose_name="Роль")
    affiliated_company = models.ForeignKey("Company", blank=True, null=True, on_delete=models.CASCADE,
                                           verbose_name="Компания")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Название")


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    short_name = models.CharField(max_length=100, verbose_name="Короткое название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    logo = models.ForeignKey("File", on_delete=models.CASCADE, null=True, blank=True)
    verified = models.BooleanField(default=False)
    departments = models.ManyToManyField(blank=True, to="Department", verbose_name="Департаменты")
    participants = models.ManyToManyField(blank=True, to="Participant", verbose_name="Участники")


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    projects = models.ManyToManyField(blank=True, to="Project", verbose_name="Проекты")


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    vacancies = models.ManyToManyField(blank=True, to="Vacancy", verbose_name="Вакансии")


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    participants = models.ManyToManyField(blank=True, to="Participant", verbose_name="Участники")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    terms = models.IntegerField(default=1, choices=TERMS, verbose_name="Условия участия")
    occupation = models.IntegerField(default=1, choices=OCCUPATION, verbose_name="Занятость")
    work_format = models.IntegerField(default=1, choices=WORK_FORMAT, verbose_name="Формат работы")


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")
    avatar = models.ForeignKey("File", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    technologies = models.TextField(verbose_name="Компетенции")


class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    file = models.ImageField(null=True, blank=True, upload_to='uploads/')


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']
