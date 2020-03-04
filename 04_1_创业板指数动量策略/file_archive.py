# coding:utf-8
# 将收益率数据导出为图片，图片保存在img文件夹中
# 分为n年累计收益率和n年当年收益率
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
fac_range=[i/100 for i in range(96,106,2)]

for l_fac in fac_range:
    for s_fac in fac_range:
        filename='./outfile/'+str(l_fac)+'_'+str(s_fac)+'.csv'
        print(filename)
        df=0
        df=pd.read_csv(filename,index_col=0)
        fig = plt.figure(figsize=(20,80))
        last_df=pd.DataFrame([[1]*10 for i in range(10)])
        for year in range(16,21):
            sub_df=df[['{}_y{}'.format(low,year) for low in range(2,12) ]]

            # 将存储上年收益率的dataframe的行列名刷新，否则列名不同会报错
            last_df.columns=sub_df.columns
            last_df.index=sub_df.index

            this_year=sub_df/last_df

            ax=fig.add_subplot(5,1,year-15)
            # 热力图的颜色板调整
            cmap = sns.cubehelix_palette(rot=-.4,as_cmap=True)
            # robust为True，会自动舍弃一些极端值
            sns.heatmap(this_year,robust=True,cmap=cmap)
            # 添加每一个表的标题
            ax.set_title('YEAR 20{}'.format(year),size=100)
            # 在图片底部添加买入条件，不过具体定位方式还没探索清楚
            ax.text(0,64,'P>Long  MA*{}\nP<Short MA*{}'.format(l_fac,s_fac),size=100)
            last_df=sub_df.copy()


        plt.savefig('./img/分年/{}_{}.png'.format(l_fac,s_fac))
        plt.close(fig)
        # plt.show()

        # print(df)
