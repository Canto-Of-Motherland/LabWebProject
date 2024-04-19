import random
import smtplib

from LabWebApp.models import Student
from email.mime.text import MIMEText
from email.utils import formataddr


def checkSignIn(request) -> dict:
    try:
        if request.session['status_sign'] == '1':
            student_id = request.session['student_id']
            result = Student.objects.get(student_id=student_id)
            student_name = result.student_name
            student_status = result.student_status
            student_photo = result.student_photo
            return {'signal': True, 'username': student_name, 'status': student_status, 'photo': student_photo}
        else:
            return {'signal': False, 'username': '未登录', 'status': '0', 'photo': 'default.jpg'}
    except KeyError:
        return {'signal': False, 'username': '未登录', 'status': '0', 'photo': 'default.jpg'}
    

def verificationGenerator() -> str:
    verification_code = ""
    
    for i in range(6):
        item = str(random.randint(0, 9))
        verification_code += item
    
    return verification_code



def sendMail(verification_code: str, address: str, function: str) -> None:
    info = '【武汉大学数据科学与智能应用实验室】您的验证码为%s，有效期5分钟，该验证码仅用于%s，请勿泄露。如非本人操作，请及时更换密码。' % (verification_code, function)
    sender = '3095631599@qq.com'
    receiver = address
    send_code = 'dzppwxmgsgsodcdg'

    message = MIMEText(info, _charset='utf-8')
    message['From'] = formataddr(("", sender))
    message['To'] = formataddr(('', receiver))
    message['Subject'] = '验证码'

    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(sender, send_code)
    server.sendmail(sender, [receiver, ], message.as_string())
    server.quit()