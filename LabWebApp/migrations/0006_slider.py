# Generated by Django 3.2.15 on 2024-01-26 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LabWebApp', '0005_student_student_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('slider_id', models.AutoField(primary_key=True, serialize=False)),
                ('slider_title', models.CharField(max_length=16)),
                ('slider_abstract', models.CharField(max_length=128)),
                ('slider_url', models.CharField(max_length=128)),
                ('slider_photo', models.CharField(max_length=16)),
            ],
        ),
    ]