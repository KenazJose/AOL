# Generated by Django 4.2 on 2023-09-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_orderupdate_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
