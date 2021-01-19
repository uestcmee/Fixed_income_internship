import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import datetime
import time

def get_html(url):
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
    try_time=0
    while try_time<10:
        try:
            res=requests.get(url,headers=headers)
            assert res.status_code==200
            break
        except:
            print('获取失败，5s后重试')
            try_time+=1
            time.sleep(5)
    # with open('./htmls/init.html','wb') as f:
    #     f.write(res.content)
    #     f.close()
    if 'res' in locals():
        return res.text
    else:
        return 0

def process_data(text):


    # with open('./htmls/init.html', 'r', encoding='utf-8') as f:
    #     text = f.read()
    #     f.close()

    soup = BeautifulSoup(text, 'lxml')
    content = soup.find_all('div', class_='content-main')[0]
    lines = content.find_all('tr')

    for index,one in enumerate(lines):

        infos = one.find_all('td')
        info_list = []
        for info in infos:
            if info.text.strip() != '' or True:  # 先不加筛选了，全部保存进去，不然列数总是出问题
                info_list.append(info.text.strip())
            pass
        if index==0:
            columns = '名称 价格范围 均价 涨跌 单位 日期 info'.split(' ')
            today_df = pd.DataFrame(columns=columns)
            # today_df = pd.DataFrame(columns=[i for i in range(len(info_list))])
        # print(today_df)
        if info_list[0] != '名称':
            # print(info_list)
            today_df.loc[today_df.shape[0]] = info_list

    today_df.iloc[:0] = today_df.iloc[:0].apply(lambda x: x.split('\n')[0]) # 名称简化
    today_df.drop('info',axis=1,inplace=True) # 去掉最后的空列
    return  today_df

def main_func():
    product_list=['copper',
 'aluminum',
 'lead',
 'zinc',
 'tin',
 'nickel',
 'stainless-steel',
 'chromium',
 'precious-metals',
 'steel',
 'manganese',
 'silicon',
 'new-energy',
 'antimony',
 'tungsten',
 'in-ge-ga',
 'bi-se-te',
 'magnesium',
 'minor-metals',
 'rare-earth',
 'metal-scraps']
    for ind,product in enumerate(product_list):
        url = 'https://hq.smm.cn/{}/fullscreen'.format(product)
        file_path='./csv/'
        file_name='{}_{}.xlsx'.format(product,str(datetime.datetime.now())[:13].replace(' ','_'))
        if file_name not in os.listdir(file_path):
            text=get_html(url)
            if text==0:
                print('{} 获取失败'.format(product))
                continue
            result_df=process_data(text)
            # result_df.to_csv(file_path+file_name,encoding='gbk')
            result_df.to_excel(file_path+file_name)
            print('保存{}信息完成({}/{})'.format(product,ind,len(product_list)))
            time.sleep(5)


if __name__ == '__main__':
    from timed_start import Timing
    print('钴价格定时爬虫')
    now=datetime.datetime.now()
    # main_func()
    Timing(title='钴价格爬虫',rule='hour>20').main_loop(func=main_func,wait_time=30)
