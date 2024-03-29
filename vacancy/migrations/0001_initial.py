# Generated by Django 3.1.2 on 2020-11-06 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('schedule_type', models.IntegerField()),
                ('employment_type', models.IntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('partnership', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='company.company')),
            ],
            options={
                'db_table': 'vacancy',
            },
        ),
        migrations.CreateModel(
            name='VacancySkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.skill')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancy.vacancy')),
            ],
            options={
                'db_table': 'vacancy_skills',
            },
        ),
        migrations.CreateModel(
            name='VacancyJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancy.vacancy')),
            ],
            options={
                'db_table': 'vacancy_jobs',
                'unique_together': {('vacancy', 'job')},
            },
        ),
        migrations.AddField(
            model_name='vacancy',
            name='jobs',
            field=models.ManyToManyField(through='vacancy.VacancyJobs', to='core.Job'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='skills',
            field=models.ManyToManyField(through='vacancy.VacancySkills', to='core.Skill'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('decision', models.CharField(choices=[('ACCEPT', 'ACCEPT'), ('DECLINE', 'DECLINE'), ('NO_ANSWER', 'NO_ANSWER')], default='NO_ANSWER', max_length=16)),
                ('seen', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='vacancy.vacancy')),
            ],
            options={
                'db_table': 'request',
            },
        ),
        migrations.CreateModel(
            name='VacancyFavorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancy.vacancy')),
            ],
            options={
                'db_table': 'vacancy_favorites',
                'unique_together': {('vacancy', 'user')},
            },
        ),
    ]
