from STG_Return import StgReturn
from DrawHeatMap import DrawPic
from InitSQL import InitSQL

class BackTest:

    def __init__(self):
        self.fac_range = [i / 100 for i in range(96, 106, 2)]
        self.year_range=range(2006,2021)
        self.fac_loop()

    def fac_loop(self):
        for l_fac in self.fac_range:
            for s_fac in self.fac_range:
                # 输出收益率文件到./outfile文件夹
                StgReturn('./data/CSI.csv',l_fac,s_fac,year_range=self.year_range)
                # 使用文件结果绘制热力图
                # DrawPic(cumflag=1,l_fac=l_fac,s_fac=s_fac)


if __name__ == '__main__':
    InitSQL('CSI.db').InitialSQL()
    BackTest()