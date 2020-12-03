# Generated by Django 3.1.1 on 2020-11-27 21:44

from django.db import migrations, models
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('listelement', '0004_auto_20201111_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='element',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='element',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
