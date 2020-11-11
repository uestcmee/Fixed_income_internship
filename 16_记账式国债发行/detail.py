import requests
from bs4 import BeautifulSoup
def get_detail(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'lxml')
    detail=soup.find('div',class_='Custom_UnionStyle')
    return detail.text

if __name__ == '__main__':
    s
    detail_url='http://gks.mof.gov.cn/ztztz/guozaiguanli/gzfxzjs/202011/t20201106_3618440.htm'
    get_detail(detail_url)