# Generated by Django 3.1.1 on 2020-10-05 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20201004_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='document',
            new_name='documento',
        ),
    ]
