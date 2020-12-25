import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import datetime


def get_html():
    url='https://hq.smm.cn/new-energy/fullscreen'
    headers={
    'Host': 'hq.smm.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
              'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://hq.smm.cn/new-energy',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }

    res=requests.get(url,headers=headers)
    # with open('./htmls/init.html','wb') as f:
    #     f.write(res.content)
    #     f.close()
    return res.text

def process_data(text):


    # with open('./htmls/init.html', 'r', encoding='utf-8') as f:
    #     text = f.read()
    #     f.close()

    soup = BeautifulSoup(text, 'lxml')
    content = soup.find_all('div', class_='content-main')[0]
    lines = content.find_all('tr')

    columns = '名称	价格范围	均价	涨跌	单位	日期'.split('	')
    today_df = pd.DataFrame(columns=columns)

    for one in lines:
        infos = one.find_all('td')
        info_list = []
        for info in infos:
            if info.text.strip() != '':
                info_list.append(info.text.strip())
            pass
        if info_list[0] != '名称':
            today_df.loc[today_df.shape[0]] = info_list

    today_df['名称'] = today_df['名称'].apply(lambda x: x.split('\n')[0])
    return  today_df

def main_func():
    file_path='./csv/'
    file_name='{}.csv'.format(str(datetime.datetime.now())[:13].replace(' ','_'))
    if file_name not in os.listdir(file_path):
        text=get_html()
        result_df=process_data(text)
        result_df.to_csv(file_path+file_name)



if __name__ == '__main__':

    from timed_start import Timing
    print('钴价格定时爬虫')
    now=datetime.datetime.now()


    Timing(title='钴价格爬虫',rule='hour>9 and hour<20 and minute<10 ').main_loop(func=main_func,wait_time=10)
