# Generated by Django 3.1.1 on 2020-11-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listelement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='price',
            field=models.DecimalField(decimal_places=2, default=6.1, max_digits=10),
        ),
    ]