# Generated by Django 3.1.2 on 2021-04-12 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0014_auto_20210412_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='short_description',
            field=models.TextField(),
        ),
    ]
