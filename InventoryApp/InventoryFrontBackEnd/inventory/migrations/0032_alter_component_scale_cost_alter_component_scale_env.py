# Generated by Django 5.0 on 2024-10-15 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_alter_component_capex_per_ugs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='scale_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='scale_env',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
