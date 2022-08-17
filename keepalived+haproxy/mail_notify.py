#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
reload(sys)
from email.MIMEText import MIMEText
import smtplib
sys.setdefaultencoding('utf-8')
import socket, fcntl, struct

def send_mail(to_list, sub, content):
    mail_host="smtp.qq.com"
    mail_user="815325223"
    mail_pass="<PASSWORD>"
    mail_postfix="qq.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        print False

def get_local_ip(ifname = 'eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret
if sys.argv[1]!="master" and sys.argv[1]!="backup" and sys.argv[1]!="fault":
    sys.exit()
else:
    notity_type = sys.argv[1]

if __name__ == '__main__':
    strcontent = get_local_ip()+ " " + notity_type+"状态被激活，请确认HAProxy服务运行状态！"
    mailto_list = ['815325223@qq.com']
    for mailto in mailto_list:
        send_mail(mailto,"HAProxy状态切换报警",strcontent.encode('utf-8'))
