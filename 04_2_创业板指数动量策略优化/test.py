import pandas as pd

df=pd.DataFrame([i for i in range(100)])
df['5avg'] = df[0].rolling(window=2).mean().shift()
print(df)
