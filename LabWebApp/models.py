from django.db import models


class News(models.Model):
    news_id = models.CharField(primary_key=True, max_length=16)
    news_title = models.CharField(max_length=128)
    news_author = models.CharField(max_length=32)
    news_photographer = models.CharField(max_length=32)
    news_category = models.CharField(max_length=1)
    news_content = models.TextField()
    news_photo = models.TextField()
    news_post_datetime = models.CharField(max_length=19)
    news_update_datetime = models.CharField(max_length=19)


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=16)
    student_name = models.CharField(max_length=128)
    student_password = models.CharField(max_length=64)
    student_photo = models.TextField()
    student_gender = models.CharField(max_length=1)
    student_grade = models.CharField(max_length=10)
    student_birthday = models.CharField(max_length=10)
    student_phone = models.CharField(max_length=11)
    student_email = models.CharField(max_length=64)
    student_github_url = models.TextField()
    student_csdn_url = models.TextField()
    student_proverb = models.TextField()
    student_self_introduction = models.TextField()
    student_major = models.CharField(max_length=64)
    student_achievement = models.TextField()
    student_graduate = models.CharField(max_length=1)
    student_status = models.CharField(max_length=1)
    student_show = models.CharField(max_length=1)


class Statistic(models.Model):
    statistic_id = models.AutoField(primary_key=True)
    statistic_year = models.CharField(max_length=3)
    statistic_achievement = models.CharField(max_length=5)
    statistic_graduate = models.CharField(max_length=5)
    statistic_team = models.CharField(max_length=5)
    statistic_project = models.CharField(max_length=3)


class Slider(models.Model):
    slider_id = models.AutoField(primary_key=True)
    slider_title = models.CharField(max_length=32)
    slider_abstract = models.CharField(max_length=128)
    slider_url = models.CharField(max_length=128)
    slider_photo = models.CharField(max_length=16)


class ResearchField(models.Model):
    research_field_content = models.TextField()
    research_field_photo = models.CharField(max_length=128)


class Thesis(models.Model):
    thesis_id = models.CharField(primary_key=True, max_length=16)
    thesis_title = models.CharField(max_length=128)
    thesis_author = models.CharField(max_length=32)
    thesis_link = models.CharField(max_length=128)
    thesis_date = models.CharField(max_length=10)

class Work(models.Model):
    work_id = models.CharField(primary_key=True, max_length=16)
    work_title = models.CharField(max_length=128)
    work_author = models.CharField(max_length=32)
    work_abstract = models.CharField(max_length=256)
    work_link = models.CharField(max_length=128)
    work_date = models.CharField(max_length=10)
    work_photo = models.CharField(max_length=16)


class Message(models.Model):
    message_id = models.CharField(primary_key=True, max_length=16)
    message_graduate = models.CharField(max_length=16)
    message_grade = models.CharField(max_length=64)
    message_link = models.CharField(max_length=128)
    message_content = models.CharField(max_length=128)
    message_date = models.CharField(max_length=10)