# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 04:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=64)),
                ('title_en', models.CharField(max_length=64)),
                ('title_fr', models.CharField(max_length=64)),
                ('logo', models.ImageField(default='category/default.jpg', upload_to='category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'blog_categories',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=256)),
                ('title_en', models.CharField(blank=True, max_length=1024)),
                ('title_fr', models.CharField(blank=True, max_length=1024)),
                ('content_en', models.TextField(blank=True)),
                ('content_fr', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('publish', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='post')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.Category')),
            ],
            options={
                'db_table': 'blog_post',
                'ordering': ('-publish',),
                'get_latest_by': 'publish',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=256)),
                ('code', models.CharField(max_length=15)),
                ('title_en', models.CharField(max_length=64)),
                ('title_fr', models.CharField(max_length=64)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='blog.Post')),
            ],
            options={
                'verbose_name_plural': 'Videos',
                'db_table': 'blog_video',
                'ordering': ('post',),
            },
        ),
    ]
