import akshare as ak
get_futures_daily_df = ak.get_futures_daily(start_date="20201220", end_date="20201225", market="SHFE", index_bar=True)
import time
import akshare as ak
dce_text = ak.match_main_contract(exchange="dce")
czce_text = ak.match_main_contract(exchange="czce")
shfe_text = ak.match_main_contract(exchange="shfe")
while True:
    time.sleep(3)
    data = ak.futures_zh_spot(
        subscribe_list=",".join([dce_text, czce_text, shfe_text]),
        market="CF",
        adjust=False)
    print(data)