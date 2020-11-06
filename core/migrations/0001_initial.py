# Generated by Django 3.1.2 on 2020-11-06 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'duty',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, unique=True)),
            ],
            options={
                'db_table': 'skill',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('qualification', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'specialization',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'university',
            },
        ),
        migrations.CreateModel(
            name='JobDuties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.duty')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
            ],
            options={
                'db_table': 'job_duties',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='duties',
            field=models.ManyToManyField(through='core.JobDuties', to='core.Duty'),
        ),
    ]
