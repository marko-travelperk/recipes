# Generated by Django 2.2.4 on 2019-08-20 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipesapp', '0005_auto_20190820_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.TextField(max_length=100),
        ),
    ]
