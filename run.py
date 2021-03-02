import os
import time


check_time = [0, 4, 8, 12, 16, 20]
last_time = time.localtime().tm_hour

while True:
    time.sleep(60)
    now_time = time.localtime().tm_hour
    if now_time != last_time:
        if now_time in check_time:
            os.system("python3 mining_data.py")
            os.system("git add *")
            os.system('git commit -m "auto commit"')
            os.system("git push -u origin main")
        last_time = now_time
