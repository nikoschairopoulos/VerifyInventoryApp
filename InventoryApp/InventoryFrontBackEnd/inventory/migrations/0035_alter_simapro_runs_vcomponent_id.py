# Generated by Django 5.0 on 2024-10-18 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0034_alter_simapro_runs_vcomponent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simapro_runs',
            name='vcomponent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='simapro_runs', to='inventory.component'),
        ),
    ]
