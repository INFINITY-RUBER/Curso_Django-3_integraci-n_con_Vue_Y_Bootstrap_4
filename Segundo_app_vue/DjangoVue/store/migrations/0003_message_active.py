# Generated by Django 3.1.1 on 2020-11-13 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
