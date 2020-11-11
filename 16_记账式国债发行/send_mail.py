import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send(title,main_text,address='793776910@qq.com'):
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "pezike@163.com"  # 用户名
    mail_pass = "pengzike"  # 口令

    sender = 'pezike@163.com'
    receivers = [address]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(main_text, 'plain', 'utf-8')
    # message['From'] = Header("菜鸟教程", 'utf-8')
    # message['To'] = Header("测试", 'utf-8')
    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    send(title='记账式国债',main_text='收到了吗')