# Generated by Django 2.1.7 on 2019-10-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20191001_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='storybodyelement',
            name='mediafile_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]