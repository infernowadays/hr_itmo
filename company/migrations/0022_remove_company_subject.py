# Generated by Django 3.1.2 on 2021-04-12 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_auto_20210412_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='subject',
        ),
    ]
