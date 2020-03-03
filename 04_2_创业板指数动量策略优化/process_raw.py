import pandas as pd
file=pd.read_csv('GE IDX.csv',names=['price','r','r+1'])
import seaborn as sns
import matplotlib.pyplot as plt
for i in file.index:
    if i !=0:

        file.loc[i]['r']=file.loc[i]['price']/file.loc[i-1]['price']-1
        file.loc[i-1]['r+1']=file.loc[i]['r']
# sns.set_style('whitegrid')
# file['r'].plot('bar')
#
# plt.show()
file.to_csv('rr.csv')
