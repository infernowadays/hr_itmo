# Generated by Django 3.1.2 on 2021-01-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0005_vacancy_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='instagram',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='pixel_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='vk',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
