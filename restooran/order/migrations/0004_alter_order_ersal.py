# Generated by Django 4.1 on 2022-08-18 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_rename_name_ersalorder_ersal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ersal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.ersalorder'),
        ),
    ]
