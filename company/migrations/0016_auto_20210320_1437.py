# Generated by Django 3.1.2 on 2021-03-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0015_auto_20210320_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, through='company.CompanyRoles', to='company.Role'),
        ),
    ]
