# coding:utf-8
# 将收益率数据导出为图片，图片保存在img文件夹中
# 分为n年累计收益率和n年当年收益率

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class DrawPic:
    def __init__(self,cumflag=1,year_range=range(2006,2021),l_fac=1.0,s_fac=1.0):

        self.l_fac=l_fac
        self.s_fac=s_fac

        # 是否累计的flag，为1则输出累计收益率，否则分年收益率
        self.cumflag=cumflag
        self.year_range=year_range

        self.draw()

    def draw(self):
        filename='./outfile/'+str(self.l_fac)+'_'+str(self.s_fac)+'.csv'
        print(filename,end='    ')
        df=pd.read_csv(filename,index_col=0)
        nyear=len(self.year_range)
        # 确定图像大小
        if nyear<5:
            figsize=(20,20*nyear)
        else:
            figsize = (20*(int(nyear/5)+1), 80)

        fig = plt.figure(figsize=figsize)
        last_df=pd.DataFrame([[1]*10 for i in range(10)])
        # 在图片底部添加买入条件
        fig.text(0,0,'P>Long  MA*{}\nP<Short MA*{}'.format(self.l_fac,self.s_fac),size=100)
        for year in self.year_range:
            sub_df=df[['{}_y{}'.format(low,year) for low in range(2,12) ]]
            # 将存储上年收益率的dataframe的行列名刷新，否则列名不同会报错
            last_df.columns=sub_df.columns
            last_df.index=sub_df.index

            this_year=sub_df/last_df
            ax=fig.add_subplot(5,3,year-self.year_range[0]-1)
            # 热力图的颜色板调整
            cmap = sns.cubehelix_palette(rot=-.4,as_cmap=True)
            # robust为True，会自动舍弃一些极端值
            if self.cumflag==1:
                weneed=sub_df
            else:
                weneed=this_year
            sns.heatmap(weneed,robust=False,cmap=cmap)  # ============== or draw sub_year
            # 添加每一个表的标题
            ax.set_title('{}'.format(year),size=100)
            # 加最大收益注释
            ax.text(0,10,'Max={},{}'.format(round(weneed.stack().max(),5),weneed.stack().idxmax()),size=50)
            last_df=sub_df.copy()

        if self.cumflag==1:
            dir_name='累计'
        else:
            dir_name='分年'
        if not os.path.exists('./img/'+dir_name):
            os.makedirs('./img/'+dir_name)
        plt.savefig('./img/'+dir_name+'/{}_{}.png'.format(self.l_fac,self.s_fac))
        plt.close(fig)
        print('====OK====')


if __name__ == '__main__':
    # Drawpic(cumflag=1)
    DrawPic(cumflag=0,fac_range=[1.01])

