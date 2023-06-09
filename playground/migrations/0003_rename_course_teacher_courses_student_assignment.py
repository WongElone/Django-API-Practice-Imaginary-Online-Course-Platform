# Generated by Django 4.1.7 on 2023-03-11 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='course',
            new_name='courses',
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('courses', models.ManyToManyField(to='playground.course')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.course')),
                ('teachers', models.ManyToManyField(to='playground.teacher')),
            ],
        ),
    ]
