# Generated by Django 3.1.7 on 2021-04-21 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_kind_navigation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navigation',
            name='tool',
        ),
    ]
