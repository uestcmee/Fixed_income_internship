import requests

try:
    res=requests.get('https://www.baidu.co')
except:
    pass
print(res)
