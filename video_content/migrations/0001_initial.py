# Generated by Django 4.2.5 on 2023-09-28 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('created_from', models.CharField(blank=True, default='Guest', max_length=100)),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('video_file_480p', models.FileField(blank=True, null=True, upload_to='videos')),
            ],
        ),
    ]