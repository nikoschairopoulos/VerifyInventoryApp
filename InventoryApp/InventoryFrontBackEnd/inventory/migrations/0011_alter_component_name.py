# Generated by Django 5.0 on 2024-03-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_component_thermal_properties'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
