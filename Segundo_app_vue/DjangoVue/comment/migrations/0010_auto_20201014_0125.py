# Generated by Django 3.1.1 on 2020-10-14 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listelement', '0001_initial'),
        ('comment', '0009_comment_element'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='listelement.element'),
        ),
    ]