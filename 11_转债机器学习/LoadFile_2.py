#coding:utf-8
import pandas as pd
import numpy as np

# 读取文件，将日期列作为行索引
# 读取收盘价(元)，记为close
# 计算日收益率，earning=(P1/P0-1)*100
class load_file():
    def __init__(self,file_name):
        self.file_name=file_name
        self.close_p=[]
        # 代码,名称,日期,开盘价(元),最高价(元),最低价(元),收盘价(元),成交额(百万),成交量(股)
    def read_file(self):
        df=pd.read_csv(self.file_name,index_col='日期')

        self.close_p=df['收盘价(元)'].to_frame()
        self.close_p.insert(1,'turnover',df['成交额(百万)'])
        self.close_p.rename(columns={'收盘价(元)':'close'},inplace=True)

        earning=[]
        self.close_p.dropna(axis=0,inplace=True)
        # 删除掉价格数据为0的日期（错误日期）
        for day in self.close_p.index:
            # print(day,self.close_p[day])
            if self.close_p.loc[day]['close']==0:
                self.close_p.drop(day,inplace=True)
        close_np=np.array(self.close_p['close'])
        # 获得前一日的收盘数据（可视为当日开盘价）
        open_np=np.roll(close_np,1)
        earning=(close_np-open_np)/open_np*100
        earning[0]=0.0
        self.close_p['earning']=earning
        return self.close_p

if __name__ == '__main__':
    file_content=load_file('./data/CSI.csv').read_file()
    print(file_content)