import pandas as pd

df=pd.DataFrame([[1,2],[3,4]],index=['a','b'])
print(df)
df.drop(df.index[0],inplace=True)
print(df)