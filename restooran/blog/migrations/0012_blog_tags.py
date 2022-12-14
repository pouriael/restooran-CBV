# Generated by Django 4.0.4 on 2022-08-12 18:51

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('blog', '0011_alter_blog_total_alter_blog_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='نسبت تشابه'),
        ),
    ]
