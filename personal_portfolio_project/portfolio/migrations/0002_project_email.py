# Generated by Django 3.0.8 on 2020-07-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='email',
            field=models.EmailField(default='NA', max_length=254),
        ),
    ]
