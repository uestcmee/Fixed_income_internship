import random
open('random2.csv','w').close()
f=open('random2.csv','a')
start=50
for i in range(1000):
    num=random.random()
    #start=start*((num-0.5)/10+1)# 随机涨跌
    start=start+1+num
    f.write(str(start)+'\n')
    print(start)

f.close()
