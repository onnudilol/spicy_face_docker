# Generated by Django 2.0.1 on 2018-01-10 01:21

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('page_id', models.CharField(unique=True, max_length=128)),
                ('url', models.URLField()),
                ('page_name', models.CharField(max_length=512)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='pictures/profile')),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to='pictures/profile')),
                ('phone_number', models.CharField(blank=True, max_length=128, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('hours', JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PagePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('page_post_id', models.CharField(max_length=32, unique=True)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimelineImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('timeline_image_id', models.CharField(max_length=32, unique=True)),
                ('created_time', models.DateTimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures/timeline')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='facebot.PagePost')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]