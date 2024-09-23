# Generated by Django 5.0 on 2024-09-23 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_component_functional_unit_component_ia_method_ghg_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggingComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.component')),
            ],
        ),
    ]
