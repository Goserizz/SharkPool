import os
import time


check_time = [0, 4, 8, 12, 16, 20]
while True:
    time.sleep(1)
    now_time = time.localtime()
    if now_time.tm_hour in check_time and now_time.tm_sec == 0:
        os.system("python3 mining_data.py")