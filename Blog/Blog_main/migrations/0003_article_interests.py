# Generated by Django 3.1.5 on 2021-01-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_main', '0002_auto_20210126_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='interests',
            field=models.ManyToManyField(to='Blog_main.Interests'),
        ),
    ]