
def detect_via_cusum_lg(ts, istart=30, threshold_times=5):
    """
    detect a time series using  cusum algorithm
    :param ts: the time series to be detected
    :param istart: the data from index 0 to index istart will be used as cold startup data to train
    :param threshold_times: the times for setting threshold
    :return:
    """
    S_h = 0
    S_l = 0
    S_list = np.zeros(istart) # 前面填充的30个空数据
    meanArray = talib.SMA(ts,timeperiod = istart)
    stdArray = talib.STDDEV(np.log(ts/meanArray),timeperiod = istart)
    for i in range(istart, len(ts)): # 这里是否应该掐头去尾？
        tslog = np.log(ts[i] / meanArray[i - 1])
        S_h_ = max(0, S_h + tslog - stdArray[i-1])
        S_l_ = min(0, S_l + tslog + stdArray[i-1])
        if S_h_> threshold_times * stdArray[i-1]:
            S_list = np.append(S_list,1) # 该点为上变点
            S_h_ = 0
        elif abs(S_l_)> threshold_times *  stdArray[i-1]:
            S_list = np.append(S_list, -1) # 该点为下变点
            S_l_ = 0
        else:
            S_list = np.append(S_list, 0) # 该点无特殊情况
        S_h = S_h_
        S_l = S_l_

    return S_list

#数据导入
dt0 = np.array(df5min["close"])
s_list = detect_via_cusum_lg(dt0,istart=30, threshold_times=10)