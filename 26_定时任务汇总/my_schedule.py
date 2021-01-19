import schedule
import time,datetime

def job():
    global t0
    t=time.time()
    print('hello',t-t0)
    t0=t
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).days.do(job)
schedule.every().monday.at("10:30").do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every(1).to(3).seconds.do(job)

t0=time.time()

while True:
    schedule.run_pending()
    # time.sleep(1)