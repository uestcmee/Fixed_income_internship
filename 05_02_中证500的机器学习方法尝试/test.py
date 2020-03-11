from LoadFile import load_file
import numpy as np
# 读取数据
close_earning=load_file('./CSI.csv').read_file()
dataset=close_earning['earning']
print(type(dataset.values))
print(np.array(dataset).reshape(-1,1))