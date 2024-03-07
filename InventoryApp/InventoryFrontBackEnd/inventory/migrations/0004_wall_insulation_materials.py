# Generated by Django 5.0 on 2024-03-05 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_factor_factor_composite_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wall_Insulation_Materials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wall_or_insulation_type', models.CharField(verbose_name=50)),
                ('component_element', models.CharField(verbose_name=50)),
                ('conductivity', models.FloatField()),
                ('capacity', models.FloatField()),
                ('density', models.FloatField()),
            ],
        ),
    ]
