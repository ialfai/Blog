# Generated by Django 3.1.5 on 2021-01-30 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_main', '0007_remove_interests_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
