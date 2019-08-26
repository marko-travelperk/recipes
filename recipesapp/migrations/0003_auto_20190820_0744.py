# Generated by Django 2.2.4 on 2019-08-20 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipesapp', '0002_auto_20190819_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='myrecipe',
            name='author',
            field=models.TextField(default='author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myrecipe',
            name='ingredients',
            field=models.TextField(default='all'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myrecipe',
            name='name',
            field=models.TextField(default='cake'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myrecipe',
            name='procedure',
            field=models.TextField(default='mix'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myrecipe',
            name='serves',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myrecipe',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]