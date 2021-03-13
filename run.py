import os
import time


check_time = [0, 4, 8, 12, 16, 20]
last_time = time.localtime().tm_hour

while True:
    time.sleep(60)
    now_time = time.localtime().tm_hour
    if now_time != last_time:
        if now_time in check_time:
            while True:
                os.system("python3 mining_data.py")
                with open('log', mode='r') as f:
                    lines = f.readlines()
                if int(lines[-1][12:14]) == now_time:
                    os.system("git add *")
                    os.system('git commit -m "auto commit"')
                    os.system("git push")
                    break
                time.sleep(1)
        last_time = now_time
