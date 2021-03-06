# Generated by Django 3.1.6 on 2021-02-12 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='standard',
            options={'ordering': ['parent__name', 'name']},
        ),
        migrations.AddField(
            model_name='supply',
            name='standards',
            field=models.ManyToManyField(blank=True, related_name='supplies', to='supply.Standard', verbose_name='規格'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='standard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supply', to='supply.standard', verbose_name='規格'),
        ),
    ]
