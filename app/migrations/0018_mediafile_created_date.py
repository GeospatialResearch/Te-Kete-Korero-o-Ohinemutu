# Generated by Django 2.1.7 on 2019-10-04 02:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_storybodyelement_mediafile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]