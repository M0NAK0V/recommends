# Generated by Django 4.1.7 on 2023-05-24 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_rename_progress_bigcourse_full_progress_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='full_progress',
            new_name='progress',
        ),
        migrations.RemoveField(
            model_name='course',
            name='min_progress',
        ),
    ]
