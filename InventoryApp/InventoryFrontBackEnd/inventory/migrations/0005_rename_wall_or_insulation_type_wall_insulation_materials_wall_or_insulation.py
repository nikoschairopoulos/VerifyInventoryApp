# Generated by Django 5.0 on 2024-03-05 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_wall_insulation_materials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wall_insulation_materials',
            old_name='wall_or_insulation_type',
            new_name='wall_or_insulation',
        ),
    ]
