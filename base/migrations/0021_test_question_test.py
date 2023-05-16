# Generated by Django 4.1.7 on 2023-05-13 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_question_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ManyToManyField(related_name='test', to='base.test'),
        ),
    ]