# Generated by Django 4.1.7 on 2023-03-25 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0017_remove_lesson_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='course/videos'),
        ),
    ]
