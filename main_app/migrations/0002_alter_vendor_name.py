# Generated by Django 4.2.7 on 2023-12-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
