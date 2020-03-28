import pandas as pd

a=pd.DataFrame([i*i for i in range(10)],index=[str('你好') for i in range(10)])
# b=pd.DataFrame([10 for i in range(10)])
# print(pd.concat([a,b],axis=1))
print(a)