from django import urls
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from LabWebApp import views
from LabWebProject import settings
from django.conf.urls import url


app_name = 'LabWebApp'
urlpatterns = [
    path('search', views.search, name='search'),
    path('user', views.userSelf, name='userSelf'),
    path('sign-in', views.signIn, name='signIn'),
    path('', views.main, name='main'),
    path('news-category/<str:news_category>/<str:page_number>', views.newsCategory, name='newsCategory'),
    path('news/<str:news_url>', views.newsDetail, name='newsDetail'),
    path('research/research-field', views.researchField, name='researchField'),
    path('research/thesis', views.researchThesis, name='researchThesis'),
    path('research/work', views.researchWork, name='researchWork'),
    path('research/platform', views.researchPlatform, name='researchPlatform'),
    path('member/teacher/detail', views.memberTeacherDetail, name='memberTeacherDetail'),
    path('member/student', views.memberStudent, name='memberStudent'),
    path('member/student/<str:student_url>', views.memberStudentDetail, name='memberStudentDetail'),
    path('about', views.about, name='about'),
    path('graduate/student', views.graduateStudent, name='graduateStudent'),
    path('graduate/message', views.graduateMessage, name='graduateMessage'),
    path('test', views.test, name='test'),
    path('admin', views.admin, name='admin'),
    path('admin/news', views.adminNews, name='adminNews'),
    path('admin/news/<str:news_url>', views.adminNewsDetail, name='adminNewsDetail'),
    path('admin/slider', views.adminSlider, name='adminSlider'),
    path('admin/statistic', views.adminStatistic, name='adminStatistic'),
    path('admin/user', views.adminUser, name='adminUser'),
    path('admin/user/<str:user_url>', views.adminUserDetail, name='adminUserDetail'),
    path('admin/research-field', views.adminResearchField, name='adminResearchField'),
    path('admin/research-thesis', views.adminResearchThesis, name='adminResearchThesis'),
    path('admin/research-work', views.adminResearchWork, name='adminResearchWork'),
    path('admin/research-work/<str:work_url>', views.adminResearchWorkDetail, name='adminResearchWorkDetail'),
    path('admin/message', views.adminMessage, name='adminMessage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.pageNotFound