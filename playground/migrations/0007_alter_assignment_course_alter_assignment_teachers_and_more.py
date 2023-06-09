# Generated by Django 4.1.7 on 2023-03-19 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0006_alter_student_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='playground.course'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='teachers',
            field=models.ManyToManyField(related_name='assignments', to='playground.teacher'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='playground.coursecategory'),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='students', to='playground.course'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='playground.course'),
        ),
    ]
