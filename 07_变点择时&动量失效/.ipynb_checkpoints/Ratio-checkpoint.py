#coding:utf-8
import pandas as pd

class ratio:

    def __init__(self):
        pass
    def cal_ratio(self,datas):
        res = []
        # 定义函数求各项回测指标
        for item in datas:
            data = datas[item]

            # 累积收益率
            strategy_cum = (data + 1).cumprod()
            # 年化收益率
            return_year = data.mean() * 252
            # 每日收益率
            return_avg = data.mean()
            # 年化波动率
            volatility = data.std() * 252 ** 0.5
            # 最大每日收益
            profit_max = data.max()
            # 最大每日损失
            loss_max = data.min()
            # 信息比率
            ir = return_year / volatility
            # 上涨天数
            num_of_up = data[data > 0].count()
            # 下跌天数
            num_of_down = data[data < 0].count()
            # 胜率
            win_rate = float(num_of_up) / (num_of_up + num_of_down)
            # 上涨时平均每日收益率
            gain_of_up = data[data > 0].mean()
            # 下跌时平均每日收益率
            loss_of_down = data[data < 0].mean()
            # 盈亏比
            profit_loss_ratio = -(gain_of_up / loss_of_down)
            # 最大回撤
            drawdown = ((strategy_cum.cummax() - strategy_cum) / strategy_cum.cummax()).max()
            # 创建一个临时的DataFrame
            tmp = pd.DataFrame(
                [ir, float((strategy_cum).tail(1)), return_year, return_avg, volatility, profit_max, loss_max,
                 num_of_up, num_of_down, win_rate, gain_of_up, loss_of_down, profit_loss_ratio, drawdown],
                columns=[data.name],
#                 index=['Information Ratio', 'Cumulative Return', 'Annualised Return', 'Average return',
#                        'Annualised Volatility', 'Maximum Daily Profit',
#                        'Maximum Daily Loss', 'Number of Up Periods', 'Number of Down Periods', 'Win Rate',
#                        'Avg Gain in Up Periods',
#                        'Avg Loss in Down Periods', 'Profit and Loss Ratio', 'Maximum Drawdown'])
                index=['信息比率', '累计收益率', '年化收益率', '每日收益率',
                       '年化波动率', '最大每日收益',
                       '最大每日损失', '上涨天数', '下跌天数', '胜率',
                       '上涨时平均每日收益率',
                       '下跌时平均每日收益率', '盈亏比', '最大回撤'])
            res.append(tmp)
        # 返回拼接好的DataFrame
        return pd.concat(res, axis=1, join='inner')

if __name__ == '__main__':
    strategy_return=[0.1,0.9,-0.5,0.2,-0.82,0.2,-0.1,-0.1]
    result = ratio().cal_ratio(pd.DataFrame(strategy_return)).round(4)
    result.columns = ['strategy_return']
    print(result)

