# Generated by Django 3.1.5 on 2021-01-29 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_main', '0006_interests_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interests',
            name='description',
        ),
    ]