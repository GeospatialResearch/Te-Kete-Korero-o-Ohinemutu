# Generated by Django 2.1.7 on 2020-05-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200514_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='affiliation',
            field=models.ManyToManyField(related_name='members', to='app.Nest'),
        ),
    ]
