# Generated by Django 4.1.3 on 2023-09-15 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Art',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.URLField()),
                ('title', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('style', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('color', models.BooleanField(default=True)),
                ('frame_type', models.CharField(max_length=50)),
                ('mods', models.BooleanField(default=False)),
                ('date_created', models.IntegerField()),
                ('film_type', models.CharField(max_length=50)),
                ('malfunction', models.BooleanField(default=False)),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='art_tag', to='thearchiveapi.tag')),
            ],
        ),
    ]
