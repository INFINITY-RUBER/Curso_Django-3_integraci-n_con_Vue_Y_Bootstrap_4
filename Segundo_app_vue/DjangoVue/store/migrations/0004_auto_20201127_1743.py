# Generated by Django 3.1.1 on 2020-11-27 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_message_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='lasname',
            new_name='lastname',
        ),
    ]