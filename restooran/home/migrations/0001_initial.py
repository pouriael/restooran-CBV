# Generated by Django 4.1 on 2022-08-14 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='اسم')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True, verbose_name='شناسه')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='تصویر')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub', to='home.category', verbose_name='زیر شاخه')),
            ],
        ),
    ]
