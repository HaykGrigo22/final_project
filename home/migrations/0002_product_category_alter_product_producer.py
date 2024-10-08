# Generated by Django 5.1 on 2024-09-13 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('home', '0001_initial'),
        ('producer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='producer.producer'),
        ),
    ]
