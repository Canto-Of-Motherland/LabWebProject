from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from LabWebApp.models import News, Student, Statistic, Slider, ResearchField, Thesis, Work, Message
from LabWebApp import util


import datetime
import os
import time
import math
import re


def pageNotFound(request, exception):
    if request.method == 'GET':
        return render(request, '404Standard.html')




def test(request):
    return render(request, 'test.html')


def search(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        key = request.GET.get('key')
        result_student = Student.objects.filter(student_name__contains=key, student_show=1)
        result_student_list = []
        list_grade = ['本科生', '研究生', '博士生']
        for student in result_student:
            student_id = student.student_id
            student_name = student.student_name
            student_grade = list_grade[int(student.student_grade[-1]) - 1]
            student_photo = student.student_photo if student.student_photo != '' else 'default.jpg'
            result_student_list.append({'student_id': student_id, 'student_name': student_name, 'student_grade': student_grade, 'student_photo': student_photo})
        
        result_news = News.objects.filter(Q(news_title__contains=key) | Q(news_content__contains=key))
        result_news_list = []
        list_news_category = ['学术科研', '团队喜讯', '讲座论坛', '生活文化']
        for news in result_news:
            news_id = news.news_id
            news_category = list_news_category[int(news.news_category) - 1]
            news_title = news.news_title
            news_post_date = news.news_post_datetime[:10]
            result_news_list.append({'news_id': news_id, 'news_category': news_category, 'news_title': news_title, 'news_post_date': news_post_date})
        
        no_result = ''
        if result_student_list == [] and result_news_list == []:
            no_result = '您要找的东西没有哦'
        return render(request, 'search.html', {'data': {'search_keyword': key, 'no_result': no_result, 'result_student': result_student_list, 'result_news': result_news_list}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def userSelf(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            return render(request, '404.html', {'error_info': '在写了在写了，还没写完'})


def signIn(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return render(request, 'signIn.html')
        else:
            return redirect('/')
    else:
        func_code = request.POST.get('func_code')
        if func_code == '0':
            try:
                email = request.POST.get('email')
                result = Student.objects.filter(student_email=email)
                if not result:
                    return JsonResponse({'status': '2'})
                else:
                    verification_code = util.verificationGenerator()
                    function = '登录'
                    util.sendMail(verification_code=verification_code, address=email, function=function)
                    time_start = int(time.time())
                    request.session['student_id'] = result.first().student_id
                    request.session['student_email'] = email
                    request.session['verification_code'] = verification_code
                    request.session['time_start'] = time_start
                    request.session['status_code'] = '0'
                    return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
        elif func_code == '1':
            try:
                email = request.POST.get('email')
                password = request.POST.get('password')
                result = Student.objects.filter(student_email=email)
                if not result:
                    return JsonResponse({'status': '2', 'message': '1'})
                else: 
                    if result.first().student_password == password:
                        request.session['student_id'] = result.first().student_id
                        request.session['status_sign'] = '1'
                        return JsonResponse({'status': '1'})
                    else:
                        return JsonResponse({'status': '2', 'message': '2'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
        elif func_code == '2':
            try:
                student_id = request.session['student_id']
                student_email = request.session['student_email']
                verification_code = request.session['verification_code']
                time_start = request.session['time_start']
                status_code = request.session['status_code']

                email = request.POST.get('email')
                code = request.POST.get('code')

                if email != student_email:
                    return JsonResponse({'status': '2', 'message': '1'})
                elif status_code == '1':
                    return JsonResponse({'status': '2', 'message': '2'})
                elif int(time_start) + 60 < int(time.time()):
                    return JsonResponse({'status': '2', 'message': '3'})
                elif code != verification_code:
                    return JsonResponse({'status': '2', 'message': '4'})
                else:
                    request.session['status_code'] = '1'
                    result = Student.objects.get(student_id=student_id)
                    request.session['student_id'] = result.student_id
                    request.session['status_sign'] = '1'
                    return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})


def main(request):
    if request.method == 'GET':
        slider_result = Slider.objects.all()
        slider_main = []
        slider_content = []
        for i, slider in enumerate(slider_result):
            if i <= 4:
                slider_main.append({'slider_title': slider.slider_title, 'slider_abstract': slider.slider_abstract, 'slider_url': slider.slider_url, 'slider_photo': slider.slider_photo})
            elif 4 < i <= 7:
                slider_content.append({'slider_title': slider.slider_title, 'slider_abstract': slider.slider_abstract, 'slider_url': slider.slider_url, 'slider_photo': slider.slider_photo})
        news_left = dict(News.objects.values('news_id', 'news_title', 'news_photo').latest('news_id'))
        news_left['news_photo'] = news_left['news_photo'].split(' | ')[0]
        news_right = list(News.objects.order_by('-news_id').values('news_id', 'news_title', 'news_post_datetime')[1:6])
        for i, news in enumerate(news_right):
            news_right[i]['news_post_datetime'] = news['news_post_datetime'][:10]
        statistic = dict(Statistic.objects.all().values('statistic_year', 'statistic_achievement', 'statistic_graduate', 'statistic_team', 'statistic_project')[0])
        check_result = util.checkSignIn(request)
        return render(request, 'main.html', {'data': {'slider_main': slider_main, 'news_left': news_left, 'news_right': news_right, 'statistic': statistic, 'slider_content': slider_content}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def newsCategory(request, news_category, page_number):
    if request.method == 'GET':
        list_news_category = ['research', 'achievement', 'lecture', 'culture']
        if news_category == 'all':
            news_result = News.objects.all()
            news_list = []
            for news in news_result:
                news_list.append({'news_id': news.news_id, 'news_title': news.news_title, 'news_post_month': news.news_post_datetime[0: 7], 'news_post_date': news.news_post_datetime[8: 10], 'news_abstract': news.news_content[0: 120]})
            num = 12
            page_number = int(page_number)
            page_total = math.ceil(len(news_list) / num)
            if page_number < math.ceil(len(news_list) / num):
                news_list.reverse()
                news_list = news_list[num * page_number - num: num * page_number]
            elif page_number == math.ceil(len(news_list) / num):
                news_list.reverse()
                news_list = news_list[num * page_number - num:]
            else:
                return redirect('/news-category/all/1')
            check_result = util.checkSignIn(request)
            return render(request, 'newsCategory.html', {'data': {'news_category': '全部新闻', 'page_number': page_number, 'page_total': page_total,'news_list': news_list}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
        elif news_category in list_news_category:
            news_category_index = str(list_news_category.index(news_category) + 1)
            news_result = News.objects.filter(news_category=news_category_index)
            news_list = []
            for news in news_result:
                news_list.append({'news_id': news.news_id, 'news_title': news.news_title, 'news_post_month': news.news_post_datetime[0: 7], 'news_post_date': news.news_post_datetime[8: 10], 'news_abstract': news.news_content[0: 120]})
            num = 12
            page_number = int(page_number)
            page_total = math.ceil(len(news_list) / num)
            if page_number < math.ceil(len(news_list) / num):
                news_list.reverse()
                news_list = news_list[num * page_number - num: num * page_number]
            elif page_number == math.ceil(len(news_list) / num):
                news_list.reverse()
                news_list = news_list[num * page_number - num:]
            else:
                return redirect('/news-category/' + news_category + '/1')
            list_news_category_chinese = ['学术科研', '团队喜讯', '讲座论坛', '生活文化']
            check_result = util.checkSignIn(request)
            return render(request, 'newsCategory.html', {'data': {'news_category': list_news_category_chinese[list_news_category.index(news_category)], 'page_number': page_number, 'page_total': page_total,'news_list': news_list}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
        else:
            return render(request, '404.html', {'error_info': '探索未知或许是件妙事……但这里真的没有什么'})


def newsDetail(request, news_url):
    if request.method == 'GET':
        try:
            news_result = News.objects.get(news_id=news_url)
            news_title = news_result.news_title
            news_category = int(news_result.news_category) - 1
            news_author = news_result.news_author
            news_photographer = news_result.news_photographer
            news_post_datetime = news_result.news_post_datetime
            
            list_news_category = ['research', 'achievement', 'lecture', 'culture']
            list_news_category_chinese = ['学术科研', '团队喜讯', '讲座论坛', '生活文化']
            news_category_url = list_news_category[news_category]
            news_category_chinese = list_news_category_chinese[news_category]

            check_result = util.checkSignIn(request)
            return render(request, 'newsDetail.html', {'data': {'news_category_url': news_category_url, 'news_category': news_category_chinese, 'news_title': news_title, 'news_author': news_author, 'news_photographer': news_photographer, 'news_post_datetime': news_post_datetime}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
        except Exception as e:
            return render(request, '404.html', {'error_info': '探索未知或许是件妙事……但这里真的没有什么'})
    else:
        news_result = News.objects.get(news_id=news_url)
        news_content = news_result.news_content
        news_content_list = []
        for paragraph in news_content.split('\n'):
            matches = re.findall(r'\(([^)]+)\)\[([^]]+)\]', paragraph)
            if matches:
                for match in matches:
                    news_content_list.append('_2_' + match[0])
                    news_content_list.append('_3_' + match[1])
            else:
                news_content_text = paragraph.replace('\r', '')
                news_content_list.append('_1_' + news_content_text)
        return JsonResponse({'news_content_list': news_content_list})


def researchField(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        return render(request, 'researchField.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
    else:
        research_field_result = ResearchField.objects.all()[0]
        research_field_content = research_field_result.research_field_content
        research_field_list = []
        for paragraph in research_field_content.split('\n'):
            matches = re.findall(r'\(([^)]+)\)\[([^]]+)\]', paragraph)
            if matches:
                for match in matches:
                    research_field_list.append('_2_' + match[0])
                    research_field_list.append('_3_' + match[1])
            else:
                research_field_text = paragraph.replace('\r', '')
                research_field_list.append('_1_' + research_field_text)
        return JsonResponse({'research_field_list': research_field_list})


def researchThesis(request):
    if request.method == 'GET':
        thesis_data_list = []
        all_thesis = Thesis.objects.all().values('thesis_title', 'thesis_author', 'thesis_date', 'thesis_link')
        total = len(all_thesis)
        for i, thesis in enumerate(all_thesis):
            thesis_number = total - i
            thesis_title = thesis['thesis_title']
            thesis_author = thesis['thesis_author']
            thesis_date = thesis['thesis_date']
            thesis_link = thesis['thesis_link']
            thesis_data_list.append({'thesis_number': thesis_number, 'thesis_title': thesis_title, 'thesis_author': thesis_author, 'thesis_date': thesis_date, 'thesis_link': thesis_link})
        thesis_data_list.reverse()
        check_result = util.checkSignIn(request)
        return render(request, 'researchThesis.html', {'data': thesis_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})

def researchWork(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        work_data_list = []
        all_work = Work.objects.all().values('work_title', 'work_author', 'work_abstract', 'work_date', 'work_link', 'work_photo')
        total = len(all_work)
        for i, work in enumerate(all_work):
            work_number = total - i
            work_title = work['work_title']
            work_author = work['work_author']
            work_abstract = work['work_abstract']
            work_date = work['work_date']
            work_link = work['work_link']
            work_photo = work['work_photo']
            work_data_list.append({'work_number': work_number, 'work_title': work_title, 'work_author': work_author, 'work_abstract': work_abstract, 'work_date': work_date, 'work_link': work_link, 'work_photo': work_photo})
        work_data_list.reverse()
        return render(request, 'researchWork.html', {'data': work_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def researchPlatform(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        return render(request, 'researchPlatform.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def memberTeacherDetail(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        return render(request, 'memberTeacherDetail.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def memberStudent(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        undergraduate_data_list = []
        postgraduate_data_list = []
        doctor_data_list = []

        all_student = Student.objects.all().values('student_id', 'student_name', 'student_grade', 'student_self_introduction', 'student_photo', 'student_graduate')
        for student in all_student:
            if student['student_graduate'] == '0':
                if student['student_grade'][-1] == '1':
                    student_id = student['student_id']
                    student_name = student['student_name']
                    student_grade = student['student_grade'][0:5] + '本科生'
                    student_self_introduction = student['student_self_introduction']
                    student_photo = student['student_photo'] if student['student_photo'] != '' else 'default.jpg'
                    undergraduate_data_list.append({'student_id': student_id, 'student_name': student_name, 'student_grade': student_grade, 'student_self_introduction': student_self_introduction, 'student_photo': student_photo})
                elif student['student_grade'][-1] == '2':
                    student_id = student['student_id']
                    student_name = student['student_name']
                    student_grade = student['student_grade'][0:5] + '研究生'
                    student_self_introduction = student['student_self_introduction']
                    student_photo = student['student_photo'] if student['student_photo'] != '' else 'default.jpg'
                    postgraduate_data_list.append({'student_id': student_id, 'student_name': student_name, 'student_grade': student_grade, 'student_self_introduction': student_self_introduction, 'student_photo': student_photo})
                elif student['student_grade'] == '3':
                    student_id = student['student_id']
                    student_name = student['student_name']
                    student_grade = student['student_grade'][0:5] + '博士生'
                    student_self_introduction = student['student_self_introduction']
                    student_photo = student['student_photo'] if student['student_photo'] != '' else 'default.jpg'
                    doctor_data_list.append({'student_id': student_id, 'student_name': student_name, 'student_grade': student_grade, 'student_self_introduction': student_self_introduction, 'student_photo': student_photo})
        undergraduate_data_list = sorted(undergraduate_data_list, key=lambda x: (x['student_grade'], x['student_name']), reverse=False)
        postgraduate_data_list = sorted(postgraduate_data_list, key=lambda x: (x['student_grade'], x['student_name']), reverse=False)
        doctor_data_list = sorted(doctor_data_list, key=lambda x: (x['student_grade'], x['student_name']), reverse=False)
        return render(request, 'memberStudent.html', {'data': {'undergraduate_data_list': undergraduate_data_list, 'postgraduate_data_list': postgraduate_data_list, 'doctor_data_list': doctor_data_list}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
    

def memberStudentDetail(request, student_url):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        try:
            list_grade = ['本科生', '研究生', '博士生']
            student_result = Student.objects.get(student_id=student_url)
            if student_result.student_show == '1':
                student_name = student_result.student_name
                student_grade = student_result.student_grade[0:5] + list_grade[int(student_result.student_grade[-1]) - 1]
                student_self_introduction = student_result.student_self_introduction
                student_gender = '男' if student_result.student_gender == '1' else '女'
                student_major = student_result.student_major
                student_email = student_result.student_email
                student_phone = student_result.student_phone
                student_graduate = '在读' if student_result.student_graduate == '0' else '已毕业'
                student_category = '毕业生' if student_result.student_graduate == '1' else '学生团队'
                student_category_link = 'memberGraduate' if student_result.student_graduate == '1' else 'memberStudent'
                student_github_url = student_result.student_github_url
                student_csdn_url = student_result.student_csdn_url
                student_achievement = student_result.student_achievement
                student_photo = student_result.student_photo if student_result.student_photo != '' else 'default.jpg'
                student_background = 'leaf.svg' if student_result.student_gender == '1' else 'blossom.svg'
                return render(request, 'memberStudentDetail.html', {
                    'data': {
                        'student_name': student_name,
                        'student_grade': student_grade,
                        'student_self_introduction': student_self_introduction,
                        'student_gender': student_gender,
                        'student_major': student_major,
                        'student_email': student_email,
                        'student_phone': student_phone,
                        'student_graduate': student_graduate,
                        'student_category': student_category,
                        'student_category_link': student_category_link,
                        'student_github_url': student_github_url,
                        'student_csdn_url': student_csdn_url,
                        'student_achievement': student_achievement,
                        'student_photo': student_photo,
                        'student_background': student_background,
                    },
                    'user': {
                        'username': check_result['username'],
                        'photo': check_result['photo']
                        }
                    }
                )
            else:
                return render(request, '404.html', {'error_info': '你找错地方了？我们这儿没这人'})
        except Exception as e:
            print(e)
            return render(request, '404.html', {'error_info': '你找错地方了？我们这儿没这人'})
        

def about(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        return render(request, 'about.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def graduateStudent(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        student_data_list = []

        all_student = Student.objects.all().values('student_id', 'student_name', 'student_grade', 'student_graduate', 'student_photo')
        list_grade = ['本科生', '研究生', '博士生']
        for student in all_student:
            if student['student_graduate'] == '1':
                student_id = student['student_id']
                student_name = student['student_name']
                student_grade = list_grade[int(student['student_grade'][-1]) - 1]
                student_photo = student['student_photo'] if student['student_photo'] != '' else 'default.jpg'
                student_data_list.append({'student_id': student_id, 'student_name': student_name, 'student_grade': student_grade, 'student_photo': student_photo})
        student_data_list = sorted(student_data_list, key=lambda x: x['student_name'], reverse=False)
        return render(request, 'graduateStudent.html', {'data': {'student_data_list': student_data_list}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})


def graduateMessage(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        return render(request, 'graduateMessage.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
    else:
        start = request.POST.get('start')
        all_message = Message.objects.all().values('message_id', 'message_graduate', 'message_grade', 'message_link', 'message_content', 'message_date')
        message_data_list = []
        for message in all_message:
            message_id = message['message_id']
            message_graduate = message['message_graduate']
            message_grade = message['message_grade']
            message_link = message['message_link']
            message_content = message['message_content']
            message_date = message['message_date']
            message_data_list.append({'message_id': message_id, 'message_graduate': message_graduate, 'message_grade': message_grade, 'message_link': message_link, 'message_content': message_content, 'message_date': message_date})
        message_data_list = sorted(message_data_list, key=lambda x: datetime.datetime.strptime(x["message_date"], "%Y-%m-%d").timestamp(), reverse=True)
        message_data_list = message_data_list[int(start):int(start) + 10] if len(message_data_list) > int(start) + 10 else message_data_list[int(start):]
        return JsonResponse({'message_data_list': message_data_list})


def admin(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                return render(request, 'adminBase.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})


def adminNews(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                news_data_list = []
                all_news = News.objects.all().values('news_id', 'news_title', 'news_post_datetime', 'news_id')
                total = len(all_news)
                for i, news in enumerate(all_news):
                    news_title = news['news_title']
                    news_post_datetime = news['news_post_datetime']
                    news_id = news['news_id']
                    news_item = {'news_num': total - i, 'news_id': news_id, 'news_title': news_title, 'news_post_datetime': news_post_datetime, 'news_id': news_id}
                    news_data_list.append(news_item)
                news_data_list.reverse()
                return render(request, 'adminNews.html', {'data': news_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        news_id = request.POST.get('news_id')
        try:
            news_result = News.objects.get(news_id=news_id)
            db_news_photo = news_result.news_photo
            if db_news_photo != '':
                db_news_photo_list = db_news_photo.split(' | ')
                for item_news_photo in db_news_photo_list:
                    item_path = os.path.join(settings.MEDIA_ROOT, item_news_photo)
                    if os.path.exists(item_path):
                        os.remove(item_path)
            news_result.delete()
            return JsonResponse({'status': '1'})
        except Exception as e:
            return JsonResponse({'status': '0', 'message': str(e)})


def adminNewsDetail(request, news_url):
    if news_url == 'add':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['signal']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    return render(request, 'adminNewsDetail.html', {'data': {'news_title': '发布新闻'}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
        else:
            try:
                news_title = request.POST.get('title')
                news_category = request.POST.get('category')
                news_author = request.POST.get('author')
                news_photographer = request.POST.get('photographer')
                news_content = request.POST.get('content')
                photos = request.FILES.getlist('photo')
                news_post_datetime = request.POST.get('post_datetime')
                news_id = 'n' + str(int(datetime.datetime.strptime(news_post_datetime, '%Y-%m-%d %H:%M:%S').timestamp()))
                news_update_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                pattern_photo = r'\((.*?)\)\[(.*?)\]'
                count = 0

                def replace(match, news_id):
                    nonlocal count
                    count += 1
                    content = match.group(2)
                    replace_content = news_id + '_' + str(count) + '.jpg'
                    return f'({replace_content})[{content}]'
                news_content = re.sub(pattern_photo, lambda match: replace(match, news_id), news_content)

                i = 0
                news_photo = ''
                for photo in photos:
                    i += 1
                    path = os.path.join(settings.MEDIA_ROOT, news_id + '_' + str(i) + '.jpg')
                    with open(path, 'wb+') as f:
                        for chunk in photo.chunks():
                            f.write(chunk)
                    if i < len(photos):
                        news_photo = news_photo + news_id + '_' + str(i) + '.jpg | '
                    else:
                        news_photo = news_photo + news_id + '_' + str(i) + '.jpg'

                news = News(
                    news_id=news_id, 
                    news_title=news_title, 
                    news_category=news_category, 
                    news_author=news_author, 
                    news_photographer=news_photographer, 
                    news_content=news_content, 
                    news_photo=news_photo, 
                    news_post_datetime=news_post_datetime, 
                    news_update_datetime=news_update_datetime
                )
                news.save()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
    elif news_url != '':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['status']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    try:
                        news_result = News.objects.get(news_id=news_url)
                        news_title = news_result.news_title
                        news_category = news_result.news_category
                        news_author = news_result.news_author
                        news_photographer = news_result.news_photographer
                        news_content = news_result.news_content
                        news_post_datetime = news_result.news_post_datetime
                        news_photo = news_result.news_photo
                        return render(request, 'adminNewsDetail.html', {
                            'data': {
                                'news_title': news_title, 
                                'news_category': news_category, 
                                'news_author': news_author, 
                                'news_photographer': news_photographer, 
                                'news_content': news_content, 
                                'news_post_datetime': news_post_datetime,
                                'news_photo': news_photo
                            }, 
                            'user': {
                                'username': check_result['username'],
                                'photo': check_result['photo']
                            }}
                        )
                    except Exception:
                        return render(request, '404.html', {'error_info': '今天的实验室，没有新闻，或许明天吧'})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})

        else:
            try:
                news_result = News.objects.get(news_id=news_url)
                try:
                    news_title = request.POST.get('title')
                    news_category = request.POST.get('category')
                    news_author = request.POST.get('author')
                    news_photographer = request.POST.get('photographer')
                    news_content = request.POST.get('content')
                    news_post_datetime = request.POST.get('post_datetime')
                    news_photo = request.POST.get('photo_path')
                    
                    db_news_title = news_result.news_title
                    db_news_category = news_result.news_category
                    db_news_author = news_result.news_author
                    db_news_photographer = news_result.news_photographer
                    db_news_content = news_result.news_content
                    db_news_post_datetime = news_result.news_post_datetime
                    db_news_photo = news_result.news_photo

                    if news_title != db_news_title:
                        news_result.news_title = news_title
                    if news_category != db_news_category:
                        news_result.news_category = news_category
                    if news_author != db_news_author:
                        news_result.news_author = news_author
                    if news_photographer != db_news_photographer:
                        news_result.news_photographer = news_photographer
                    if news_content != db_news_content:
                        pattern_photo = r'\((.*?)\)\[(.*?)\]'
                        count = 0
                        def replace(match, news_id):
                            nonlocal count
                            count += 1
                            content = match.group(2)
                            replace_content = news_id + '_' + str(count) + '.jpg'
                            return f'({replace_content})[{content}]'
                        news_content = re.sub(pattern_photo, lambda match: replace(match, news_url), news_content)
                        news_result.news_content = news_content
                    if news_post_datetime != db_news_post_datetime:
                        news_result.news_post_datetime = news_post_datetime
                        news_result.news_id = 'n' + str(int(datetime.datetime.strptime(news_post_datetime, '%Y-%m-%d %H:%M:%S').timestamp()))
                        news_url = news_result.news_id
                        pattern_photo = re.compile(news_url)
                        news_result.news_content = pattern_photo.sub(news_result.news_id, db_news_content)
                        if db_news_photo != '':
                            news_result.news_photo = pattern_photo.sub(news_result.news_id, db_news_photo)
                        
                        news_delete_result = News.objects.filter(news_id=news_url)
                        if db_news_photo != '':
                            db_news_photo_list = db_news_photo.split(' | ')
                            for item_news_photo in db_news_photo_list:
                                item_path = os.path.join(settings.MEDIA_ROOT, item_news_photo)
                                if os.path.exists(item_path):
                                    os.rename(item_path, os.path.join(settings.MEDIA_ROOT, news_result.news_id + item_news_photo[item_news_photo.index('_'):]))
                        news_delete_result.delete()
                    if news_photo != db_news_photo:
                        if db_news_photo != '':
                            db_news_photo_list = db_news_photo.split(' | ')
                            for item_news_photo in db_news_photo_list:
                                item_path = os.path.join(settings.MEDIA_ROOT, item_news_photo)
                                if os.path.exists(item_path):
                                    os.remove(item_path)
                        photos = request.FILES.getlist('photo')
                        i = 0
                        news_photo = ''
                        for photo in photos:
                            i += 1
                            path = os.path.join(settings.MEDIA_ROOT, news_url + '_' + str(i) + '.jpg')
                            with open(path, 'wb+') as f:
                                for chunk in photo.chunks():
                                    f.write(chunk)
                            if i < len(photos):
                                news_photo = news_photo + news_url + '_' + str(i) + '.jpg | '
                            else:
                                news_photo = news_photo + news_url + '_' + str(i) + '.jpg'
                        news_result.news_photo = news_photo
                    news_result.news_update_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    news_result.save()
                    return JsonResponse({'status': '1'})
                except Exception as e:
                    return JsonResponse({'status': '0', 'message': str(e)})
            except Exception:
                return render(request, '404.html', {'error_info': '今天的实验室，没有新闻，或许明天吧'})


def adminSlider(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                slider_data_list_1 = []
                slider_data_list_2 = []
                all_slider = Slider.objects.all().values('slider_title', 'slider_abstract', 'slider_url', 'slider_photo')
                i = 0
                j = 0
                for slider in all_slider:
                    if i < 5:
                        i += 1
                        slider_title = slider['slider_title']
                        slider_abstract = slider['slider_abstract']
                        slider_url = slider['slider_url']
                        slider_photo = slider['slider_photo']
                        slider_item_1 = {'slider_num': i, 'slider_title': slider_title, 'slider_abstract': slider_abstract, 'slider_url': slider_url, 'slider_photo': slider_photo}
                        slider_data_list_1.append(slider_item_1)
                    elif j < 3:
                        j += 1
                        slider_title = slider['slider_title']
                        slider_url = slider['slider_url']
                        slider_photo = slider['slider_photo']
                        slider_item_2 = {'slider_num': j, 'slider_title': slider_title, 'slider_url': slider_url, 'slider_photo': slider_photo}
                        slider_data_list_2.append(slider_item_2)
                return render(request, 'adminSlider.html', {'data': {'slider_1': slider_data_list_1, 'slider_2': slider_data_list_2}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        func_code = request.POST.get('func_code')
        if func_code == '1':
            slider_id = request.POST.get('item_number')
            slider_title = request.POST.get('slider_title')
            slider_abstract = request.POST.get('slider_abstract')
            slider_url = request.POST.get('slider_url')
        
            slider_result = Slider.objects.get(slider_id=slider_id)
            slider_result.slider_title = slider_title
            slider_result.slider_abstract = slider_abstract
            slider_result.slider_url = slider_url

            photo = request.FILES.get('slider_photo')
            if photo:
                slider_photo = 's' + slider_id + '.jpg'
                path = os.path.join(settings.MEDIA_ROOT, slider_photo)
                with open(path, 'wb+') as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
            slider_result.save()
            return JsonResponse({'status': '1'})
        elif func_code == '2':
            slider_id = str(int(request.POST.get('item_number')) + 5)
            slider_title = request.POST.get('slider_title')
            slider_url = request.POST.get('slider_url')

            slider_result = Slider.objects.get(slider_id=slider_id)
            slider_result.slider_title = slider_title
            slider_result.slider_url = slider_url

            photo = request.FILES.get('slider_photo')
            if photo:
                slider_photo = 's' + slider_id + '.jpg'
                path = os.path.join(settings.MEDIA_ROOT, slider_photo)
                with open(path, 'wb+') as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
            slider_result.save()
            return JsonResponse({'status': '1'})
        

def adminStatistic(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                statistic = dict(Statistic.objects.all().values('statistic_year', 'statistic_achievement', 'statistic_graduate', 'statistic_team', 'statistic_project')[0])
                return render(request, 'adminStatistic.html', {'data': statistic, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        func_code = request.POST.get('func_code')
        if func_code == '1':
            statistic = request.POST.get('statistic')
            statistic_id = request.POST.get('statistic_id')
            statistic_result = Statistic.objects.get(statistic_id='1')
            if statistic_id == '1':
                statistic_result.statistic_year = statistic
            elif statistic_id == '2':
                statistic_result.statistic_achievement = statistic
            elif statistic_id == '3':
                statistic_result.statistic_graduate = statistic
            elif statistic_id == '4':
                statistic_result.statistic_team = statistic
            elif statistic_id == '5':
                statistic_result.statistic_project = statistic
            statistic_result.save()
            return JsonResponse({})
        elif func_code == '2':
            statistic = request.POST.get('statistic')
            statistic_id = request.POST.get('statistic_id')
            statistic_result = Statistic.objects.get(statistic_id='1')
            statistic_data = 0
            if statistic_id == '3':
                statistic_result.statistic_graduate = Student.objects.filter(student_show='1', student_graduate='1').count()
                statistic_data = statistic_result.statistic_graduate
            elif statistic_id == '4':
                statistic_result.statistic_team = Student.objects.filter(student_show='1', student_graduate='0').count()
                statistic_data = statistic_result.statistic_team
            statistic_result.save()
            return JsonResponse({'statistic_data': statistic_data})



def adminUser(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                user_data_list = []
                all_user = Student.objects.all().values('student_id', 'student_name', 'student_graduate', 'student_status', 'student_show')
                for user in all_user:
                    user_id = user['student_id']
                    user_name = user['student_name']
                    user_graduate = user['student_graduate']
                    user_status = user['student_status']
                    user_show = user['student_show']
                    user_item = {'user_id': user_id, 'user_name': user_name, 'user_graduate': user_graduate, 'user_status': user_status, 'user_show': user_show}
                    user_data_list.append(user_item)
                for i in range(len(user_data_list)):
                    user_data_list[i]['user_num'] = i + 1
                return render(request, 'adminUser.html', {'data': user_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        func_code = request.POST.get('func_code')
        if func_code == '1':
            user_id = request.POST.get('user_id')
            user_item = request.POST.get('user_item')
            user_attr = request.POST.get('user_attr')
            user_result = Student.objects.get(student_id=user_id)
            if user_item == 'item_graduate':
                user_result.student_graduate = user_attr
            elif user_item == 'item_status':
                user_result.student_status = user_attr
            elif user_item == 'item_show':
                user_result.student_show = user_attr
            user_result.save()
            return JsonResponse({})
        elif func_code == '2':
            user_id = request.POST.get('user_id')
            try:
                user_result = Student.objects.get(student_id=user_id)
                db_user_photo = user_result.student_photo
                if db_user_photo != '':
                    item_path = os.path.join(settings.MEDIA_ROOT, db_user_photo)
                    if os.path.exists(item_path):
                        os.remove(item_path)
                user_result.delete()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})


def adminUserDetail(request, user_url):
    if user_url == 'add':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['signal']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    return render(request, 'adminUserDetail.html', {'data': {}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
        else:
            try:
                student_id = 'u' + str(int(time.time()))
                student_name = request.POST.get('name')
                student_password = student_id
                student_gender = request.POST.get('gender')
                student_grade = request.POST.get('grade') + '级' + request.POST.get('degree')
                student_birthday = request.POST.get('birthday')
                student_phone = request.POST.get('phone')
                student_email = request.POST.get('email')
                student_github_url = request.POST.get('github_url')
                student_csdn_url = request.POST.get('csdn_url')
                student_proverb = request.POST.get('proverb')
                student_self_introduction = request.POST.get('self_introduction')
                student_major = request.POST.get('major')
                student_achievement = request.POST.get('achievement')
                student_graduate = '0'
                student_status = '0'
                student_show = '1'

                photo = request.FILES.get('photo')
                student_photo = ''
                if photo:
                    student_photo = student_id + '.jpg'
                    path = os.path.join(settings.MEDIA_ROOT, student_photo)
                    with open(path, 'wb+') as f:
                        for chunk in photo.chunks():
                            f.write(chunk)
            
                student = Student(
                    student_id=student_id, 
                    student_name=student_name, 
                    student_password=student_password, 
                    student_photo=student_photo, 
                    student_gender=student_gender, 
                    student_grade=student_grade, 
                    student_birthday=student_birthday, 
                    student_phone=student_phone, 
                    student_email=student_email, 
                    student_github_url=student_github_url, 
                    student_csdn_url=student_csdn_url, 
                    student_proverb=student_proverb, 
                    student_self_introduction=student_self_introduction, 
                    student_major=student_major, 
                    student_achievement=student_achievement,
                    student_graduate=student_graduate, 
                    student_status=student_status,
                    student_show=student_show
                )
                
                student.save()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
    elif user_url != '':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['signal']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    try:
                        student_result = Student.objects.get(student_id=user_url)
                        student_name = student_result.student_name
                        student_photo = student_result.student_photo
                        student_gender = student_result.student_gender
                        student_grade_info = student_result.student_grade.split('级')
                        student_grade = student_grade_info[0]
                        student_degree = student_grade_info[1]
                        student_birthday = student_result.student_birthday
                        student_phone = student_result.student_phone
                        student_email = student_result.student_email
                        student_github_url = student_result.student_github_url
                        student_csdn_url = student_result.student_csdn_url
                        student_proverb = student_result.student_proverb
                        student_self_introduction = student_result.student_self_introduction
                        student_major = student_result.student_major
                        student_achievement = student_result.student_achievement
                        return render(request, 'adminUserDetail.html', {
                            'data': {
                                'student_name': student_name, 
                                'student_photo': student_photo, 
                                'student_gender': student_gender, 
                                'student_grade': student_grade, 
                                'student_degree': student_degree, 
                                'student_birthday': student_birthday, 
                                'student_phone': student_phone, 
                                'student_email': student_email,  
                                'student_github_url': student_github_url, 
                                'student_csdn_url': student_csdn_url, 
                                'student_proverb': student_proverb,
                                'student_self_introduction': student_self_introduction, 
                                'student_major': student_major, 
                                'student_achievement': student_achievement
                            }, 
                            'user': {
                                'username': check_result['username'],
                                'photo': check_result['photo']
                            }}
                        )
                    except Exception as e:
                        return render(request, '404.html', {'error_info': '你找错地方了？我们这儿没这人'})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
        else:
            try:
                student_result = Student.objects.get(student_id=user_url)
                try:
                    student_name = request.POST.get('name')
                    student_photo = request.POST.get('photo_path')
                    student_gender = request.POST.get('gender')
                    student_grade = request.POST.get('grade') + '级' + request.POST.get('degree')
                    student_birthday = request.POST.get('birthday')
                    student_phone = request.POST.get('phone')
                    student_email = request.POST.get('email')
                    student_github_url = request.POST.get('github_url')
                    student_csdn_url = request.POST.get('csdn_url')
                    student_proverb = request.POST.get('proverb')
                    student_self_introduction = request.POST.get('self_introduction')
                    student_major = request.POST.get('major')
                    student_achievement = request.POST.get('achievement')

                    db_student_name = student_result.student_name
                    db_student_photo = student_result.student_photo
                    db_student_gender = student_result.student_gender
                    db_student_grade = student_result.student_grade
                    db_student_birthday = student_result.student_birthday
                    db_student_phone = student_result.student_phone
                    db_student_email = student_result.student_email
                    db_student_github_url = student_result.student_github_url
                    db_student_csdn_url = student_result.student_csdn_url
                    db_student_proverb = student_result.student_proverb
                    db_student_self_introduction = student_result.student_self_introduction
                    db_student_major = student_result.student_major
                    db_student_achievement = student_result.student_achievement

                    if student_name != db_student_name:
                        student_result.student_name = student_name
                    if student_gender != db_student_gender:
                        student_result.student_gender = student_gender
                    if student_grade != db_student_grade:
                        student_result.student_grade = student_grade
                    if student_birthday != db_student_birthday:
                        student_result.student_birthday = student_birthday
                    if student_phone != db_student_phone:
                        student_result.student_phone = student_phone
                    if student_email != db_student_email:
                        student_result.student_email = student_email
                    if student_github_url != db_student_github_url:
                        student_result.student_github_url = student_github_url
                    if student_csdn_url != db_student_csdn_url:
                        student_result.student_csdn_url = student_csdn_url
                    if student_proverb != db_student_proverb:
                        student_result.student_proverb = student_proverb
                    if student_self_introduction != db_student_self_introduction:
                        student_result.student_self_introduction = student_self_introduction
                    if student_major != db_student_major:
                        student_result.student_major = student_major
                    if student_achievement != db_student_achievement:
                        student_result.student_achievement = student_achievement
                    if student_photo != db_student_photo:
                        if db_student_photo != '':
                            path_delete = os.path.join(settings.MEDIA_ROOT, db_student_photo)
                            if os.path.exists(path_delete):
                                os.remove(path_delete)
                        photo = request.FILES.get('photo')
                        if photo:
                            path_save = os.path.join(settings.MEDIA_ROOT, user_url + '.jpg')
                            student_result.student_photo = student_result.student_id + '.jpg'
                            with open(path_save, 'wb+') as f:
                                for chunk in photo.chunks():
                                    f.write(chunk)
                        else:
                            student_result.student_photo = ''
                    student_result.save()
                    return JsonResponse({'status': '1'})
                except Exception as e:
                    return JsonResponse({'status': '0', 'message': str(e)})
            except Exception as e:
                return render(request, '404.html', {'error_info': '你找错地方了？我们这儿没这人'})


def adminResearchField(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                result_research_field = ResearchField.objects.all()[0]
                research_field_content = result_research_field.research_field_content
                research_field_photo = result_research_field.research_field_photo
                return render(request, 'adminResearchField.html', {'data': {'research_field_content': research_field_content, 'research_field_photo': research_field_photo}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        try:
            research_field_content = request.POST.get('content')
            research_field_photo = request.POST.get('photo_path')

            research_field_result = ResearchField.objects.all()[0]
            db_research_field_content = research_field_result.research_field_content
            db_research_field_photo = research_field_result.research_field_photo

            if research_field_content != db_research_field_content:
                pattern_photo = r'\((.*?)\)\[(.*?)\]'
                count = 0
                def replace(match):
                    nonlocal count
                    count += 1
                    content = match.group(2)
                    replace_content = 'r' + str(count) + '.jpg'
                    return f'({replace_content})[{content}]'
                research_field_content = re.sub(pattern_photo, replace, research_field_content)
                research_field_result.research_field_content = research_field_content
            if research_field_photo != db_research_field_photo:
                if db_research_field_photo != '':
                    db_research_field_photo_list = db_research_field_photo.split(' | ')
                    for item_research_field_photo in db_research_field_photo_list:
                        item_path = os.path.join(settings.MEDIA_ROOT, item_research_field_photo)
                        if os.path.exists(item_path):
                            os.remove(item_path)
                photos = request.FILES.getlist('photo')
                i = 0
                research_field_photo = ''
                for photo in photos:
                    i += 1
                    path = os.path.join(settings.MEDIA_ROOT, 'r' + str(i) + '.jpg')
                    with open(path, 'wb+') as f:
                        for chunk in photo.chunks():
                            f.write(chunk)
                    if i < len(photos):
                        research_field_photo = research_field_photo + 'r' + str(i) + '.jpg | '
                    else:
                        research_field_photo = research_field_photo + 'r' + str(i) + '.jpg'
                research_field_result.research_field_photo = research_field_photo
            research_field_result.save()
            return JsonResponse({'status': '1'})
        except Exception as e:
            return JsonResponse({'status': '0', 'message': str(e)})


def adminResearchThesis(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                thesis_data_list = []
                all_thesis = Thesis.objects.all().values('thesis_id', 'thesis_title', 'thesis_author', 'thesis_date', 'thesis_link')
                total = len(all_thesis)
                for i, thesis in enumerate(all_thesis):
                    thesis_number = total - i
                    thesis_id = thesis['thesis_id']
                    thesis_title = thesis['thesis_title']
                    thesis_author = thesis['thesis_author']
                    thesis_date = thesis['thesis_date']
                    thesis_link = thesis['thesis_link']
                    thesis_data_list.append({'thesis_number': thesis_number, 'thesis_id': thesis_id, 'thesis_title': thesis_title, 'thesis_author': thesis_author, 'thesis_date': thesis_date, 'thesis_link': thesis_link})
                thesis_data_list.reverse()
                return render(request, 'adminResearchThesis.html', {'data': thesis_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        func_code = request.POST.get('func_code')
        if func_code == '1':
            thesis_id = request.POST.get('thesis_id')
            signal = request.POST.get('signal')
            thesis_title = request.POST.get('thesis_title')
            thesis_author = request.POST.get('thesis_author')
            thesis_date = request.POST.get('thesis_date')
            thesis_link = request.POST.get('thesis_link')
            if signal == '0':
                thesis = Thesis(
                    thesis_id='t' + str(int(datetime.datetime.strptime(thesis_date, '%Y-%m-%d').timestamp())),
                    thesis_title=thesis_title,
                    thesis_author=thesis_author,
                    thesis_link=thesis_link,
                    thesis_date=thesis_date
                    )
                thesis.save()
                return JsonResponse({'status', '1'})
            elif signal == '1':
                try:
                    thesis_result = Thesis.objects.get(thesis_id=thesis_id)
                    thesis_result.thesis_title = thesis_title
                    thesis_result.thesis_author = thesis_author
                    thesis_result.thesis_link = thesis_link
                    if thesis_date != thesis_result.thesis_date:
                        thesis_result_delete = Thesis.objects.get(thesis_id=thesis_id)
                        thesis_result.thesis_id = 't' + str(int(datetime.datetime.strptime(thesis_date, '%Y-%m-%d').timestamp()))
                        thesis_result.thesis_date = thesis_date
                        thesis_result_delete.delete()
                    thesis_result.save()
                    return JsonResponse({'status': '1'})
                except Exception as e:
                    return JsonResponse({'status': '0', 'message': str(e)})
        elif func_code == '2':
            thesis_date = request.POST.get('thesis_date')
            thesis_id = 't' + str(int(datetime.datetime.strptime(thesis_date, '%Y-%m-%d').timestamp()))
            try:
                thesis_result = Thesis.objects.get(thesis_id=thesis_id)
                thesis_result.delete()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})


def adminResearchWork(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                work_data_list = []
                all_work = Work.objects.all().values('work_id', 'work_title', 'work_link', 'work_date')
                total = len(all_work)
                for i, work in enumerate(all_work):
                    work_id = work['work_id']
                    work_title = work['work_title']
                    work_link = work['work_link']
                    work_date = work['work_date']
                    work_item = {'work_num': total - i, 'work_id': work_id, 'work_title': work_title, 'work_link': work_link, 'work_date': work_date}
                    work_data_list.append(work_item)
                work_data_list.reverse()
                return render(request, 'adminResearchWork.html', {'data': work_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        work_id = request.POST.get('work_id')
        try:
            work_result = Work.objects.get(work_id=work_id)
            db_work_photo = work_result.work_photo
            if db_work_photo != '':
                item_path = os.path.join(settings.MEDIA_ROOT, db_work_photo)
                if os.path.exists(item_path):
                    os.remove(item_path)
            work_result.delete()
            return JsonResponse({'status': '1'})
        except Exception as e:
            return JsonResponse({'status': '0', 'message': str(e)})
   

def adminResearchWorkDetail(request, work_url):
    if work_url == 'add':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['signal']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    return render(request, 'adminResearchWorkDetail.html', {'data': {'work_title': '新增著作'}, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
        else:
            try:
                work_title = request.POST.get('title')
                work_author = request.POST.get('author')
                work_abstract = request.POST.get('abstract')
                work_date = request.POST.get('date')
                work_link = request.POST.get('link')
                work_id = 'w' + str(int(datetime.datetime.strptime(work_date, '%Y-%m-%d').timestamp()))

                photo = request.FILES.get('photo')
                work_photo = ''
                if photo:
                    work_photo = work_id + '.jpg'
                    path = os.path.join(settings.MEDIA_ROOT, work_photo)
                    with open(path, 'wb+') as f:
                        for chunk in photo.chunks():
                            f.write(chunk)

                work = Work(
                    work_id=work_id,
                    work_title=work_title,
                    work_author=work_author,
                    work_abstract=work_abstract,
                    work_date=work_date,
                    work_link=work_link,
                    work_photo=work_photo
                )

                work.save()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
    elif work_url != '':
        if request.method == 'GET':
            check_result = util.checkSignIn(request)
            if not check_result['signal']:
                return redirect('/sign-in')
            else:
                if check_result['status'] == '1':
                    try:
                        work_result = Work.objects.get(work_id=work_url)
                        work_title = work_result.work_title
                        work_author = work_result.work_author
                        work_abstract = work_result.work_abstract
                        work_date = work_result.work_date
                        work_link = work_result.work_link
                        work_photo = work_result.work_photo
                        return render(request, 'adminResearchWorkDetail.html', {
                            'data': {
                                'work_title': work_title,
                                'work_author': work_author,
                                'work_abstract': work_abstract,
                                'work_date': work_date,
                                'work_link': work_link,
                                'work_photo': work_photo,
                            },
                            'user': {
                                'username': check_result['username'],
                                'photo': check_result['photo'],
                            }
                        })
                    except Exception as e:
                        return render(request, '404.html', {'error_info': '说不定你可以写一下这本书哦~'})
                else:
                    return render(request, '404.html', {'error_info': '门上了锁，但可惜你没钥匙'})
        else:
            try:
                work_result = Work.objects.get(work_id=work_url)
                try:
                    work_title = request.POST.get('title')
                    work_author = request.POST.get('author')
                    work_abstract = request.POST.get('abstract')
                    work_date = request.POST.get('date')
                    work_link = request.POST.get('link')
                    work_photo = request.POST.get('photo_path')

                    db_work_id = work_result.work_id
                    db_work_title = work_result.work_title
                    db_work_author = work_result.work_author
                    db_work_abstract = work_result.work_abstract
                    db_work_date = work_result.work_date
                    db_work_link = work_result.work_link
                    db_work_photo = work_result.work_photo

                    if work_title != db_work_title:
                        work_result.work_title = work_title
                    if work_author != db_work_author:
                        work_result.work_author = work_author
                    if work_abstract != db_work_abstract:
                        work_result.work_abstract = work_abstract
                    if work_link != db_work_link:
                        work_result.work_link = work_link
                    if work_date != db_work_date:
                        work_result.work_date = work_date
                        work_result.work_id = 'w' + str(int(datetime.datetime.strptime(work_date, '%Y-%m-%d').timestamp()))
                        work_url = work_result.work_id
                        if db_work_photo == '':
                            work_result.work_photo = work_result.work_id + '.jpg'
                        
                        work_delete_result = Work.objects.filter(work_id=db_work_id)
                        work_delete_result.delete()
                    if work_photo != db_work_photo:
                        if db_work_photo != '':
                            path_delete = os.path.join(settings.MEDIA_ROOT, db_work_photo)
                            if os.path.exists(path_delete):
                                os.remove(path_delete)
                        photo = request.FILES.get('photo')
                        path_save = os.path.join(settings.MEDIA_ROOT, work_url + '.jpg')
                        with open(path_save, 'wb+') as f:
                            for chunk in photo.chunks():
                                f.write(chunk)
                    work_result.save()
                    return JsonResponse({'status': '1'})
                except Exception as e:
                    return JsonResponse({'status': '0', 'message': str(e)})
            except:
                return render(request, '404.html', {'error_info': '说不定你可以写一下这本书哦~'})
            

def adminMessage(request):
    if request.method == 'GET':
        check_result = util.checkSignIn(request)
        if not check_result['signal']:
            return redirect('/sign-in')
        else:
            if check_result['status'] == '1':
                message_data_list = []
                all_message = Message.objects.all().values('message_id', 'message_graduate', 'message_grade', 'message_link', 'message_content', 'message_date')
                for message in all_message:
                    message_id = message['message_id']
                    message_graduate = message['message_graduate']
                    message_grade = message['message_grade']
                    message_link = message['message_link']
                    message_content = message['message_content']
                    message_date = message['message_date']
                    message_data_list.append({'message_id': message_id, 'message_graduate': message_graduate, 'message_grade': message_grade, 'message_link': message_link, 'message_content': message_content, 'message_date': message_date})
                message_data_list = sorted(message_data_list, key=lambda x: datetime.datetime.strptime(x["message_date"], "%Y-%m-%d").timestamp(), reverse=True)
                for i in range(len(message_data_list)):
                    message_data_list[i]['message_num'] = i + 1
                return render(request, 'adminMessage.html', {'data': message_data_list, 'user': {'username': check_result['username'], 'photo': check_result['photo']}})
            else:
                return render(request, 'adminMessage.html', {'error_info': '门上了锁，但可惜你没钥匙'})
    else:
        func_code = request.POST.get('func_code')
        if func_code == '1':
            graduate = request.POST.get('graduate')
            try:
                student_result = Student.objects.get(student_name=graduate)
                grade_list = ['本科', '硕士', '博士']
                student_grade = student_result.student_grade[0:5] + grade_list[int(student_result.student_grade[-1]) - 1]
                return JsonResponse({'status': '1', 'student_grade': student_grade})
            except:
                return JsonResponse({'status': '0', 'student_grade': '无该生信息'})
        elif func_code == '2':
            graduate = request.POST.get('graduate')
            try:
                student_result = Student.objects.get(student_name=graduate)
                student_link = request.POST.get('link_base')[0:-13] + 'member/student/' + student_result.student_id
                return JsonResponse({'status': '1', 'student_link': student_link})
            except:
                return JsonResponse({'status': '0', 'student_link': '无该生信息'})
        elif func_code == '3':
            message_id = 'm' + str(int(datetime.datetime.now().timestamp()))
            message_graduate = request.POST.get('graduate')
            message_grade = request.POST.get('grade')
            message_link = request.POST.get('link')
            message_content = request.POST.get('message')
            message_date = request.POST.get('date')

            message = Message(
                message_id = message_id,
                message_graduate = message_graduate,
                message_grade = message_grade,
                message_link = message_link,
                message_content = message_content,
                message_date = message_date
            )

            message.save()
            return JsonResponse({'status': '1'})
        elif func_code == '4':
            message_id = request.POST.get('itemId')
            try:
                message_result = Message.objects.get(message_id=message_id)
                message_graduate = request.POST.get('graduate')
                message_grade = request.POST.get('grade')
                message_link = request.POST.get('link')
                message_content = request.POST.get('message')
                message_date = request.POST.get('date')

                if message_graduate != message_result.message_graduate:
                    message_result.message_graduate = message_graduate
                if message_grade != message_result.message_grade:
                    message_result.message_grade = message_grade
                if message_link != message_result.message_link:
                    message_result.message_link = message_link
                if message_content != message_result.message_content:
                    message_result.message_content = message_content
                if message_date != message_result.message_date:
                    message_result.message_date = message_date
                    
                message_result.save()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})
        elif func_code == '5':
            message_id = request.POST.get('itemId')
            try:
                message_result = Message.objects.get(message_id=message_id)
                message_result.delete()
                return JsonResponse({'status': '1'})
            except Exception as e:
                return JsonResponse({'status': '0', 'message': str(e)})

