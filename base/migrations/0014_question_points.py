# Generated by Django 4.1.7 on 2023-05-12 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_option_remove_question_options_question_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='points',
            field=models.IntegerField(default=1),
        ),
    ]