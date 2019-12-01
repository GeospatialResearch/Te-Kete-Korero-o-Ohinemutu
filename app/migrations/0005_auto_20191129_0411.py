# Generated by Django 2.1.7 on 2019-11-29 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20191129_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='story_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.StoryType'),
        ),
        migrations.AddField(
            model_name='storybodyelement',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ContentType'),
        ),
    ]
