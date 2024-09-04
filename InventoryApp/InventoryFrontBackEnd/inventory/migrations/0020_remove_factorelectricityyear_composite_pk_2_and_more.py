# Generated by Django 5.0 on 2024-09-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_factorelectricityyear_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='factorelectricityyear',
            name='composite_pk_2',
        ),
        migrations.AddConstraint(
            model_name='factorelectricityyear',
            constraint=models.UniqueConstraint(fields=('country', 'year'), name='composite_pk_2'),
        ),
    ]
