#coding:utf-8
import pandas as pd

class load_file():
    def __init__(self,file_name):

        self.file_name=file_name
        self.close_p=[]
        # 代码,名称,日期,开盘价(元),最高价(元),最低价(元),收盘价(元),成交额(百万),成交量(股)
    def read_file(self):
        df=pd.read_csv(self.file_name,index_col='日期')

        self.close_p=df['收盘价(元)']
        # print(close_p.head(10))
        last_p=1000
        earning=[]
        for day in self.close_p.index:
            if self.close_p[day]==0:
                self.close_p.drop(day,inplace=True)
        close_list=self.close_p.tolist()
        for now_idx in close_list:
            earning.append(((now_idx/last_p)-1)*100)
            last_p=now_idx
        self.close_p=self.close_p.to_frame()
        self.close_p['earning']=earning
        self.close_p.rename(columns={'收盘价(元)':'close'},inplace=True)
        return self.close_p
if __name__ == '__main__':
    file_content=load_file('./data/GE IDX.csv').read_file()
    print(file_content)