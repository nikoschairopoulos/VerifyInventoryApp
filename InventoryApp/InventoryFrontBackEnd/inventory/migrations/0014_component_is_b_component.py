# Generated by Django 5.0 on 2024-04-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_component_bibliography_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='IS_B_COMPONENT',
            field=models.BooleanField(null=True),
        ),
    ]
