# Generated by Django 2.1.7 on 2020-05-14 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200513_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nest',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]