# Generated by Django 3.2.16 on 2023-06-12 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
