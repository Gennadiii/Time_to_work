from datetime import time
from datetime import datetime
import os.path

direction = os.path.expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')
spent = input('Input time You\'ve already been here: ')
now = str(datetime.time(datetime.now()))[:5]
additional_time = 0

if spent[0] == '*':
	spent = spent[1:]
	additional_time = int(spent[:spent.find('*')])
	spent = spent[spent.find('*')+1:]

if spent[-1] == '+':
	spent = spent[:-1]
	min_spent = int(spent[-2:]) + int(spent[:-3])*60
	min_now = int(now[-2:]) + int(now[:-3])*60
	time_of_coming = str(min_now - min_spent)
	doc = open(direction,'w')
	doc.write(time_of_coming)
	doc.close()

min_spent = int(spent[-2:]) + int(spent[:-3])*60
min_now = int(now[-2:]) + int(now[:-3])*60

time_to_work_int = 8*60 + additional_time - min_spent
time_to_work = str(time_to_work_int // 60) + ':' + '0'*(time_to_work_int % 60 < 10) + str(time_to_work_int % 60)

doc = open(direction,'r')
time_of_coming = int(doc.readline())
doc.close()

time_to_leave_int = min_now + time_to_work_int
time_to_leave = str(time_to_leave_int // 60) + ':' + '0'*(time_to_leave_int % 60 < 10) + str(time_to_leave_int % 60)

fun_time_int = time_to_leave_int - time_of_coming - min_spent - time_to_work_int
fun_time = str(fun_time_int // 60) + ':' + '0'*(fun_time_int % 60 < 10) + str(fun_time_int % 60)

print('\n\n' + 'Time left to work: ' + time_to_work)
print('\n\n' + 'Time of fun: ' + fun_time)
input('\n\n' + 'Time to leave: ' + time_to_leave + '\n\n')
