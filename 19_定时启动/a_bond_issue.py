# 星期三自动开始获取国债数据
# 开始获取后弹窗提示
# 这里还是不要传参的好，如果有取消延时的情况直接递归好了

from bond_remind_tkinter import BondRemind
from timed_start import Timing

print('国债发行检测')

# 最开始担心吧类的初始化函数带入进去会每次循环都初始化一次
# 好像这样直接把class代入进去，也不会每次都初始化
# 还是稳妥一点

br=BondRemind() # 先初始化债券提醒，一个初始信息
Timing(title='国债发行检测',rule='weekday<=5 and tim>"09:00:00" and tim<"20:00:00"').main_loop(func=br.main_fun,wait_time=1)