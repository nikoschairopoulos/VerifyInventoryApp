# Generated by Django 5.0 on 2024-10-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_alter_simapro_runs_vcomponent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simapro_runs',
            name='IS_MAIN_INVENTORY',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simapro_runs',
            name='SHEET_TYPE',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
