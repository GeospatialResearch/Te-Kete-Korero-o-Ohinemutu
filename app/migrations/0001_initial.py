# Generated by Django 2.2.12 on 2020-06-10 22:07

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atua',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Nest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creatednests', to=settings.AUTH_USER_MODEL)),
                ('kaitiaki', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('summary', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('approx_time', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('is_detectable', models.BooleanField(blank=True, default=True, null=True)),
                ('atua', models.ManyToManyField(to='app.Atua')),
                ('being_edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='being_edited', to=settings.AUTH_USER_MODEL)),
                ('last_edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_edited', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoryGeomAttrib',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('description', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('style', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='StoryType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebsiteTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=300, unique=True)),
                ('eng', models.CharField(max_length=300)),
                ('mao', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='WhanauGroupInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(blank=True, null=True)),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL)),
                ('nest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='app.Nest')),
            ],
        ),
        migrations.CreateModel(
            name='StoryGeomAttribMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('media_type', models.CharField(choices=[('IMG', 'IMG'), ('AUDIO', 'AUDIO'), ('VIDEO', 'VIDEO')], default='IMG', max_length=20)),
                ('mediafile_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('media_description', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('geom_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.StoryGeomAttrib')),
                ('mediafile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MediaFile')),
            ],
        ),
        migrations.CreateModel(
            name='StoryBodyElement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('element_type', models.CharField(choices=[('TEXT', 'TEXT'), ('IMG', 'IMG'), ('AUDIO', 'AUDIO'), ('VIDEO', 'VIDEO'), ('GEOM', 'GEOM')], default='TEXT', max_length=20)),
                ('text', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('mediafile_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('media_description', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('order_position', models.IntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ContentType')),
                ('geom_attr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.StoryGeomAttrib')),
                ('mediafile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MediaFile')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Story')),
            ],
        ),
        migrations.AddField(
            model_name='story',
            name='story_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.StoryType'),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('DRAFT', 'DRAFT'), ('SUBMITTED', 'SUBMITTED'), ('REVIEWED', 'REVIEWED'), ('ACCEPTED', 'ACCEPTED'), ('PUBLISHED', 'PUBLISHED'), ('UNPUBLISHED', 'UNPUBLISHED')], default='SUBMITTED', max_length=20)),
                ('status_modified_on', models.DateTimeField(auto_now=True)),
                ('nest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='app.Nest')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='app.Story')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('pepeha', models.TextField(blank=True, max_length=2000, null=True)),
                ('bio', models.TextField(blank=True, max_length=2000, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('membership_number', models.CharField(blank=True, max_length=100, null=True)),
                ('affiliation', models.ManyToManyField(related_name='members', to='app.Nest')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='nest',
            name='kinship_sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Sector'),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('geomtype', models.IntegerField(choices=[(0, 'POINT'), (1, 'LINE'), (2, 'POLYGON'), (3, 'RASTER')], default=0)),
                ('copyright_text', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('assigned_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shared_with', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=None, null=True, size=None)),
                ('style', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('co_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coauthors', to=settings.AUTH_USER_MODEL)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coauthers', to='app.Story')),
            ],
        ),
        migrations.AddConstraint(
            model_name='publication',
            constraint=models.UniqueConstraint(fields=('story', 'nest'), name='unique_story_nest'),
        ),
    ]
