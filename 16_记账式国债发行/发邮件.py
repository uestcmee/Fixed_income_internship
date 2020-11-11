# coding:utf-8
# 1. 获得网页内容
# 2. 建立数据库，先仅仅获取第一条内容
# 3. 对比，有差异进行发送邮件

import requests
from bs4 import BeautifulSoup
from send_mail import send
import time,datetime
from detail import get_detail
# import sys
# if len(sys.argv)==1:
#     address = '793776910@qq.com'
# else:
#     address=sys.argv[1]
# print(address)

address=input('请输入邮箱地址：')

def get_url():
    url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/'
    res=requests.get(url)
    text=res.content
    # with open('main.html','wb') as f:
    #     f.write(text)
    #     f.close()
    soup=BeautifulSoup(text,'lxml')
    info_list=soup.find_all('ul',class_='liBox')[0]
    # 获取单个的数据，目前先只考虑第一个
    for one in info_list.find_all('li'):
        title=one.text
        date=one.span.text
        href=url+one.a.attrs['href'][2:]
        return [title,date,href]


init_info=get_url()
if address[-1]==' ':
    details = get_detail(init_info[2])
    send(title=init_info[0], main_text=details)
else:
    address=address.strip()
print('目前最新:',init_info[0])
while True:
    info=get_url()
    if info!=init_info:
        details=get_detail(info[2])
        print('有新消息：{}'.format(info[0]))
        send(title=info[0],main_text=details,address=address)
    else:
        print('\r{} 无变化'.format(datetime.datetime.now()))
    time.sleep(30)