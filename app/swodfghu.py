from datetime import datetime

now = str(datetime.now())

year = now[0:4]
month = now[5:7]
day = now[8:10]
hour = now[11:13]
minute = now[14:16]
second = now[17:19]

print(f"{year} | {month} | {day} | {hour} | {minute} | {second}")
print(now)