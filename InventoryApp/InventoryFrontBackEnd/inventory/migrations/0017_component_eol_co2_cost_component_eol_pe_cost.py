# Generated by Django 5.0 on 2024-08-30 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_factor_comments_factor_source_carbonintensitydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='eol_co2_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='component',
            name='eol_pe_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
