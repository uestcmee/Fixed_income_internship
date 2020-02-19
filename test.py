a=[['2015/1/1',1,3],['2016/1/1',2,4]]
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
scatter=pd.DataFrame(a)
scatter=scatter.set_index(0)
print(scatter)
scatter.index=pd.DatetimeIndex(scatter.index)
print(scatter)
print(scatter.describe())

sns.set_style('whitegrid')
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(scatter)
ax.bar(scatter.index,height=scatter[1],width=200)
plt.show()
