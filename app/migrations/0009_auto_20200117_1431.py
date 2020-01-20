# Generated by Django 2.1.7 on 2020-01-17 14:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200117_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storygeomattrib',
            name='description',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='storygeomattrib',
            name='name',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True),
        ),
    ]
