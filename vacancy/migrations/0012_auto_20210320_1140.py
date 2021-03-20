# Generated by Django 3.1.2 on 2021-03-20 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0011_auto_20210310_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='pixel_id',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='vk',
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='short_description',
            field=models.TextField(default='lalala'),
            preserve_default=False,
        ),
    ]
