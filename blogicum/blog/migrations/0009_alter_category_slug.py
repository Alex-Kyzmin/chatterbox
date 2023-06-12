# Generated by Django 3.2.16 on 2023-05-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20230521_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор'),
        ),
    ]