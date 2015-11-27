from datetime import datetime
from time import sleep
import json
from selenium import webdriver
from os.path import expanduser
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains

today = 0
yestarday = 1
username = 'g.mishchevskyi'
password = '*'

password = password[:4] + password[-4:]

password = chr(ord(password[0])-9) + chr(ord(password[1])+10) + chr(ord(password[2])-12) + chr(ord(password[3])-5) + chr(ord(password[4])) + chr(ord(password[5])+3) + chr(ord(password[6])-1) + chr(ord(password[7])-4)

now = datetime.now()
day_of_week = datetime.weekday(now)

def time2int(time):
	return int( time[:2] )*60 + int( time[3:] )

def int2time(integer):
	return str(integer // 60) + ':' + '0'*(integer % 60 < 10) + str(integer % 60)

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')
current_time_int = time2int( str(datetime.time(datetime.now()))[:5] )

driver = webdriver.Chrome(expanduser(r'~\Dropbox\Work\Python\chromedriver.exe'))
driver.get('https://' + username + ':' + password + '@' + 'portal-ua.globallogic.com/officetime/')
driver.implicitly_wait(600)

def time_worked_for(day):
	chart = driver.find_element_by_css_selector("#bar > svg > rect:nth-child(" + str(25 + day_of_week - day) + ")")
	ActionChains(driver).move_to_element(chart).perform()
	time_worked_raw = driver.find_element_by_css_selector("#bar > div").text
	time_worked = time_worked_raw[:5]
	driver.quit()
	return time2int(time_worked)

time_worked_int = time_worked_for(today)
time_of_coming = current_time_int - time_worked_int

data = json.load(open(txt, 'r'))

if data['day_of_week'] != day_of_week:
	last_additional_time = data['additional_time']
	if day_of_week != 0:
		worked_yestarday = time_worked_for(yestarday)
		print( 'Yestarday worked: ' + int2time(worked_yestarday) )
	else:
		worked_yestarday = 8*60 + last_additional_time

	additional_time = last_additional_time + ( 8*60 - worked_yestarday )
	if additional_time < 0: additional_time = 0
	data = { 'day_of_week':day_of_week, 'time_of_coming':time_of_coming, 'additional_time':additional_time }
	json.dump(data, open(txt, 'w'))

data = json.load(open(txt, 'r'))

time_of_coming = data['time_of_coming']
additional_time = data['additional_time']

time_to_work_int = 8*60 - time_worked_int + additional_time
time_to_work = int2time(time_to_work_int)

time_to_leave_int = current_time_int + time_to_work_int
time_to_leave = int2time(time_to_leave_int)

fun_time_int = time_to_leave_int - time_of_coming - time_worked_int - time_to_work_int
fun_time = int2time(fun_time_int)

print('\n\n' + 'Time worked: ' + int2time(time_worked_int) )
print('\n\n' + 'Time left to work: ' + time_to_work)
print('\n\n' + 'Time of fun: ' + fun_time)
print('\n\n' + 'Time to leave: ' + time_to_leave + '\n\n')
if additional_time != 0: print( '\n\n' + 'Additional_time : ' + str(additional_time) )

input()
