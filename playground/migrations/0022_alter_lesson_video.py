# Generated by Django 4.1.7 on 2023-03-25 06:43

from django.db import migrations, models
import playground.validators


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0021_alter_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='course/videos'),
        ),
    ]
