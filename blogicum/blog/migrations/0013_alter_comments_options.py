# Generated by Django 3.2.16 on 2023-06-11 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20230609_1917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('created_at',)},
        ),
    ]