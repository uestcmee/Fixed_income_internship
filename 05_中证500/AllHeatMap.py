# coding:utf-8
# 绘制每个乘数组合的最大收益率对应的热力图
# 通过读取outfile文件夹中的csv文件中的收益率数据
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
outfiles=os.listdir('./outfile')

# 所选择的乘数的范围
fac_list=[96,98,99,100,101,102,103,104,105,106]
df_all=pd.DataFrame(index=[str(i/100) for i in fac_list],columns=[str(i/100) for i in fac_list])
# print(df_all)
maxinfo=[]
for file in outfiles:
    [l_fac,s_fac]=file[:-4].split('_') # 获取文件名中的乘数参数
    filename = './outfile/' + str(l_fac) + '_' + str(s_fac) + '.csv'
    # print(filename, end='    ')
    df = pd.read_csv(filename, index_col=0)
    # 在图片底部添加买入条件
    year=2020 # 只要2020的数据
    weneed = df[['{}_y{}'.format(low, year) for low in range(2, 12)]]
    [maxx,coor]=[round(weneed.stack().max(), 5), weneed.stack().idxmax()]
    maxinfo.append([l_fac,s_fac,maxx,coor[0],int(coor[1].split('_')[0])])
    df_all.loc[l_fac][s_fac]=maxx
info_df=pd.DataFrame(maxinfo)
info_df.to_csv('./global_out_file/max_info.csv')
df_all.to_csv('./global_out_file/max_r_heat.csv')
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
# 没有默认保存
# plt.savefig('Summarize Cumulative Return.png')
plt.show()