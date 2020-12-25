#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

with open('./htmls/init.html','r',encoding='utf-8') as f:
    text=f.read()
    f.close()

soup=BeautifulSoup(text,'lxml')
content=soup.find_all('div',class_='content-main')[0]
lines=content.find_all('tr')
# print(lines)
print(len(lines))


# In[64]:


columns='名称	价格范围	均价	涨跌	单位	日期'.split('\n')
today_df=pd.DataFrame(columns=columns)

for one in lines:
    infos=one.find_all('td')
    info_list=[]
    for info in infos:
        if info.text.strip()!='':
            info_list.append(info.text.strip())
        pass
    if info_list[0]!='名称':
        today_df.loc[today_df.shape[0]] = info_list
    
today_df['名称']=today_df['名称'].apply(lambda x:x.split('\n')[0])
today_df


# In[29]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




