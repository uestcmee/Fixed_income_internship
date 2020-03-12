import time
import pandas
from STG_Return import StgReturn
def fetch_lookback_data(lf=1,sf=1,lm=30,sm=5):
    # df=pandas.read_csv('compare.csv')
    # # print(df)
    # res=[df.iloc[:,0].tolist(),df.iloc[:,1].tolist(),df.iloc[:,2].tolist()]
    # return res
    df=StgReturn(file_name='./data/CSI.csv',l_fac=lf,s_fac=sf,lma =lm,sma =sm).main_loop()
    # print(df)
    res=[df.index.tolist(),df.iloc[:,0].tolist(),df.iloc[:,1].tolist()]
    return res
def get_time():
    str_time = time.strftime("%Y{}%m{}%d{} %X")
    return str_time.format("年", "月", "日")

if __name__ == '__main__':

    data = fetch_lookback_data()
    print(data)
