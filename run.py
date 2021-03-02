import os
import time


check_time = [0, 4, 8, 12, 16, 20]
now_time = time.localtime().tm_hour
for temp_time in [4, 8, 12, 16, 20, 24]:
    if now_time < temp_time:
        next_time = temp_time
if next_time == 24:
    next_time = 0

while True:
    time.sleep(60)
    now_time = time.tm_hour
    if now_time == next_time:
        os.system("python3 mining_data.py")
        os.system("git add *")
        os.system('git commit -m "auto commit"')
        os.system("git push -u origin main")
        next_time = (next_time + 4) % 24
