# Generated by Django 3.1.1 on 2020-10-06 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20201005_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='sex',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO'), ('O', 'OTRO')], default='M', max_length=1),
        ),
    ]
