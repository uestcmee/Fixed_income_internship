import requests
from bs4 import BeautifulSoup
def get_detail(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'lxml')
    detail=soup.find('div',class_='my_conboxzw')
    return detail.text

if __name__ == '__main__':
    detail_url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/202011/t20201106_3618440.htm'
    get_detail(detail_url)