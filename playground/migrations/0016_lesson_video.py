# Generated by Django 4.1.7 on 2023-03-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0015_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='course/videos'),
        ),
    ]
