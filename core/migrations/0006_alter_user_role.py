# Generated by Django 4.1.7 on 2023-03-25 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ST', 'Student'), ('TE', 'Teacher')], default='ST', max_length=2),
        ),
    ]