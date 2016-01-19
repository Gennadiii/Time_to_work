from my_lib import *
import json

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')
data = json.load(open(txt, 'r'))

time_worked = data['worked_from_home']
while True:
	print( str(time_worked) + '\n' )
	sleep(60)
	time_worked += 1
	data['worked_from_home'] = time_worked
	json.dump(data, open(txt, 'w'))
