# Generated by Django 4.1.7 on 2023-03-11 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0004_remove_course_updated_at_assignment_allow_submit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, null=True, to='playground.course'),
        ),
    ]
