from my_lib import *
import json

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')

false_alarm = input('Start tracking? ')

if len(false_alarm) != 0:
	data = json.load(open(txt, 'r'))
	data['fun_time'] -= data['temp_fun_time']
	data['temp_fun_time'] = 0
	json.dump(data, open(txt, 'w'))
	print('Fun time is rolled back')
	sleep(1)
else:
	fun_time = -3
	while True:
		sleep(3)
		data = json.load(open(txt, 'r'))
		data['fun_time'] += 1
		data['temp_fun_time'] += 1
		json.dump(data, open(txt, 'w'))
		fun_time += 1
		print( str(fun_time) + '\n' )
