# Generated by Django 4.1.3 on 2023-10-03 03:57

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='pic')),
                ('title', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('style', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('color', models.BooleanField(default=True)),
                ('frame_type', models.CharField(max_length=50)),
                ('mods', models.BooleanField(default=False)),
                ('date_created', models.DateField()),
                ('film_type', models.CharField(max_length=50)),
                ('malfunction', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Fan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ArtTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thearchiveapi.art')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thearchiveapi.tag')),
            ],
        ),
        migrations.AddField(
            model_name='art',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='art', through='thearchiveapi.ArtTag', to='thearchiveapi.tag'),
        ),
    ]
