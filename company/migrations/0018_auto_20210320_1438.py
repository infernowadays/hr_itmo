# Generated by Django 3.1.2 on 2021-03-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20210320_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.TextField(default='MVP'),
            preserve_default=False,
        ),
    ]
