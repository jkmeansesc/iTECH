# 邮件发送功能
from django.core.mail import send_mail

def send_mails(subject, message, from_email, recipient_list):
    # subject = "Blog update"
    # message = "xxx has updated the blog. Please check it out."
    # from_email = "2079459973@qq.com"

    # recipient_list = ["zhengkangwu666@gmail.com", ]
    send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)


