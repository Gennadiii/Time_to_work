from datetime import time
from datetime import datetime

spent = input('Input time You\'ve already been here: ')
now = str(datetime.time(datetime.now()))[:5]

min_spent = int(spent[-2:]) + int(spent[:-3])*60
min_now = int(now[-2:]) + int(now[:-3])*60

time_to_work_int = 8*60 - min_spent
time_to_work = str(time_to_work_int // 60) + ':' + '0'*(time_to_work_int % 60 < 10) + str(time_to_work_int % 60)

time_to_leave_int = min_now + time_to_work_int
time_to_leave = str(time_to_leave_int // 60) + ':' + '0'*(time_to_leave_int % 60 < 10) + str(time_to_leave_int % 60)

print('\n\n' + 'Time left to work: ' + time_to_work)
input('\n\n' + 'Time to leave: ' + time_to_leave)
