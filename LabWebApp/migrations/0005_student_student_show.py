# Generated by Django 3.2.15 on 2023-10-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LabWebApp', '0004_rename_students_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_show',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
