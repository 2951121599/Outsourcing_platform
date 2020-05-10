from django.core.mail import send_mail


def send_mail_remind(project_name):
    subject = "众包网站项目中标提醒"  # 题目
    html_message = """
        <p>尊敬的用户 您好</p>
        <p>您参与竞标的项目 %s,已被发包方选中,请及时与发包方联系,感谢你的使用! </p>
    """ % project_name
    # recipient_list = '2951121599@qq.com'  # 接收者邮件列表
    send_mail(subject, "", "2951121599@qq.com", html_message=html_message, recipient_list=['2951121599@qq.com'])
