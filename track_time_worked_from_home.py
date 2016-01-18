from my_lib import *
import json

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')

time_worked = 0
while True:
	sleep(60)
	data = json.load(open(txt, 'r'))
	data['worked_from_home'] += 1
	json.dump(data, open(txt, 'w'))
	time_worked += 1
	print( str(time_worked) + '\n' )
