# Generated by Django 4.1.7 on 2023-05-13 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_question_options_alter_question_question_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.CharField(choices=[('1', 'текст'), ('2', 'Два варианта ответов'), ('3', 'Три варианта ответов'), ('4', 'Четыре варианта ответов')], default='1', max_length=1),
        ),
    ]
