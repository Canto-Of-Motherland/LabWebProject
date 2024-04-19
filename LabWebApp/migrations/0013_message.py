# Generated by Django 3.2.15 on 2024-04-16 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LabWebApp', '0012_rename_statistics_statistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('message_graduate', models.CharField(max_length=16)),
                ('message_major', models.CharField(max_length=64)),
                ('message_link', models.CharField(max_length=128)),
                ('message_content', models.CharField(max_length=128)),
                ('message_date', models.CharField(max_length=10)),
            ],
        ),
    ]
