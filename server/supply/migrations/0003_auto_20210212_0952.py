# Generated by Django 3.1.6 on 2021-02-12 00:52

from django.db import migrations


def make_many_supplies(apps, schema_editor):
    """
        Adds the Standard object in Supply.standard to the
        many-to-many relationship in Supply.standards
    """
    Supply = apps.get_model('supply', 'Supply')

    for supply in Supply.objects.all():
        if supply.standard:
            supply.standards.add(supply.standard)

class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0002_auto_20210212_0950'),
    ]

    operations = [
        migrations.RunPython(make_many_supplies),
    ]