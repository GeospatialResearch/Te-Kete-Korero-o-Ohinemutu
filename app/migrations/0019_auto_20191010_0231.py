# Generated by Django 2.1.7 on 2019-10-10 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_mediafile_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='summary',
            field=models.TextField(max_length=1000),
        ),
    ]