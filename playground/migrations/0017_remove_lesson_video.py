# Generated by Django 4.1.7 on 2023-03-25 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0016_lesson_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='video',
        ),
    ]
