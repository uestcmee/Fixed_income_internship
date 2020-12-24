#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import re
import sys

# In[2]:
if len(sys.argv)>1:
    file_name=sys.argv[1]
else:
    file_name='衡泰&手工_简化.xlsx'
df=pd.read_excel(file_name,sheet_name='衡泰')
df2=pd.read_excel(file_name,sheet_name='手工')
df_sg_s=df2[['代码','简称','占资规模','持仓规模']]
df_sg_s
df_ht_s=df[['代码','简称','占资规模','持仓规模']]
df_ht_s


# In[3]:


code_list=[]
for one in df_ht_s.groupby('代码'):
    if one[1].iloc[0,1]!=0:
        code_list.append(one[0])
        if len(one[1])>1:
#             print(one[1])
            pass
print(len(code_list))


# In[4]:


for df in [df_ht_s,df_sg_s]:
    df['代码']=df['代码'].apply(lambda x:int(re.findall('\d+',str(x))[0]))


# In[5]:


def pre_process(df_ht_s):
    df_ht_all=df_ht_s.groupby('代码').sum()
    df_ht_all=df_ht_all[df_ht_all.sum(axis=1)!=0]
    df_ht_all['代码']=df_ht_all.index
    df_ht_all.index=([i for i in range(len(df_ht_all))])
    return df_ht_all
ht=pre_process(df_ht_s)
sg=pre_process(df_sg_s)


# In[ ]:





# In[6]:


joint=set(ht['代码'])&set(sg['代码']) # 两者中相同的代码
res=sg.set_index('代码').loc[joint]==ht.set_index('代码').loc[joint] 


# In[15]:


res_index=res[res.sum(axis=1)!=2].index # 相同代码中存在差异的个券


diff_df=pd.concat([ht.set_index('代码').loc[res_index],sg.set_index('代码').loc[res_index]],axis=1)
diff_df.columns=['衡泰占资规模','衡泰持仓规模','手工占资规模','手工持仓规模']
diff_df.insert(0,'简称',df_ht_s.set_index('代码').loc[res_index]['简称'])
diff_df


# In[16]:


# 只出现在衡泰中的
ht_only=set(ht['代码'])-set(sg['代码']) # 两者中相同的代码
ht_only_df=ht.set_index('代码').loc[ht_only]

ht_only_df.columns=['衡泰占资规模','衡泰持仓规模']
ht_only_df['简称']=df_ht_s.set_index('代码').loc[ht_only]['简称']
ht_only_df


# In[17]:


# 只出现在手工中的
sg_only=set(sg['代码'])-set(ht['代码']) # 两者中相同的代码
sg_only_df=sg.set_index('代码').loc[sg_only]
sg_only_df.columns=['手工占资规模','手工持仓规模']

sg_only_df['简称']=df_sg_s.set_index('代码').loc[sg_only]['简称']
sg_only_df


# In[62]:


diff_df_all=diff_df.append([ht_only_df,sg_only_df])

diff_df_all.fillna(0,inplace=True)
diff_df_all['占资差']=diff_df_all['衡泰占资规模']-diff_df_all['手工占资规模']
diff_df_all['持仓差']=diff_df_all['衡泰持仓规模']-diff_df_all['手工持仓规模']
diff_df_all.loc['汇总']=diff_df_all.iloc[:,1:].sum(axis=0)
diff_df_all


# In[64]:


diff_df_all.to_excel('衡泰手工差异.xlsx')


# In[ ]:




