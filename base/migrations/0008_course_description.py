# Generated by Django 4.1.7 on 2023-05-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_course_achievement_progress_achievement_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(default='', max_length=255),
        ),
    ]
