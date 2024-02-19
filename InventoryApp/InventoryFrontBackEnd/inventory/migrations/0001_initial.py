# Generated by Django 5.0 on 2024-02-14 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('component_type', models.CharField(db_column='type', max_length=50)),
                ('component_subtype', models.CharField(db_column='subtype', max_length=50, null=True)),
                ('capex_per_ugs', models.FloatField(db_column='capex/u.g.s.')),
                ('opex_per_capex', models.FloatField(db_column='opex_per_capex')),
                ('embodied_co2_per_ugs', models.FloatField(db_column='embodied_co2/u.g.s.')),
                ('embodied_pe_per_ugs', models.FloatField(db_column='embodied_pe/u.g.s.')),
                ('lifetime', models.FloatField()),
                ('pref_cost', models.FloatField(db_column='Pref_cost')),
                ('pref_env', models.FloatField(db_column='Pref_env')),
                ('scale_cost', models.FloatField()),
                ('scale_env', models.FloatField()),
                ('major_upgrade_point', models.FloatField()),
                ('major_upgrade_share', models.FloatField()),
                ('annual_performance_degradation', models.FloatField()),
                ('replace_or_die', models.CharField(max_length=20)),
                ('SHEET_TYPE', models.CharField(max_length=20)),
                ('IS_MAIN_INVENTORY', models.BooleanField()),
                ('bibliography', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('project_name', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to=settings.AUTH_USER_MODEL)),
                ('components', models.ManyToManyField(blank=True, related_name='inventories', to='inventory.component')),
            ],
        ),
    ]
