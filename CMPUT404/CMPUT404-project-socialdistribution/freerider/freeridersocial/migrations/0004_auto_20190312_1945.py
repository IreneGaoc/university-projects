# Generated by Django 2.1.5 on 2019-03-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeridersocial', '0003_auto_20190310_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(editable=False),
        ),
    ]