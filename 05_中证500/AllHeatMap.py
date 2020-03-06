# coding:utf-8
# 绘制每个乘数组合的最大收益率对应的热力图
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
outfiles=os.listdir('./outfile')

fac_list=[96,98,99,100,101,102,103,104,105,106]
df_all=pd.DataFrame(index=[str(i/100) for i in fac_list],columns=[str(i/100) for i in fac_list])
# print(df_all)
maxinfo=[]
for file in outfiles:
    [l_fac,s_fac]=file[:-4].split('_')
    filename = './outfile/' + str(l_fac) + '_' + str(s_fac) + '.csv'
    # print(filename, end='    ')
    df = pd.read_csv(filename, index_col=0)
    # 在图片底部添加买入条件
    for year in range(2020, 2021):# 只要2020的数据
        weneed = df[['{}_y{}'.format(low, year) for low in range(2, 12)]]
        [maxx,coor]=[round(weneed.stack().max(), 5), weneed.stack().idxmax()]
        maxinfo.append([l_fac,s_fac,maxx,coor[0],int(coor[1].split('_')[0])])
    df_all.loc[l_fac][s_fac]=maxx
info_df=pd.DataFrame(maxinfo)
info_df.to_csv('max_info.csv')
df_all.to_csv('max_r_heat.csv')
df_all.fillna(value=1,inplace=True)
print(df_all)

fig=plt.figure(figsize=(80,80))
ax=fig.add_subplot(111)
ax.set_title('2005-2020 Cumulative Return',size=50)
cmap = sns.cubehelix_palette(rot=-.4, as_cmap=True)
sns.heatmap(df_all,cmap=cmap)
plt.ylabel('Long MA Multiplier', fontdict={'family' : 'Times New Roman', 'size'   : 32})
plt.xlabel('Short MA Multiplier', fontdict={'family' : 'Times New Roman', 'size'   : 32})

label_y = ax.get_yticklabels()
plt.setp(label_y , rotation = 360,size=20)
label_x = ax.get_xticklabels()
plt.setp(label_x ,size=20)
plt.show()