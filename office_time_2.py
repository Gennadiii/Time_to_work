import shutil
from datetime import datetime
import json
from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from my_lib import *

now = datetime.now()
day_of_week = datetime.weekday(now)

today = 0
yestarday = 1
username = '*'
password = '*'
days_length = 8*60

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time.txt')
txt_backup = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time_backup.txt')

driver = webdriver.Chrome(expanduser(r'~\Dropbox\Work\Python\chromedriver.exe'))
driver.get('https://' + username + ':' + password + '@' + 'portal-ua.globallogic.com/officetime/')
driver.implicitly_wait(30)

def time2int(time):
    return int( time[:2] )*60 + int( time[3:] )

def int2time(integer):
	flag = False
	if integer < 0:
		integer = -integer
		flag = True
	return flag*'-' + str(int(integer // 60)) + ':' + '0'*(integer % 60 < 10) + str(integer % 60)

def time_worked_for(day):
    chart = driver.find_element_by_css_selector("#bar > svg > rect:nth-child(" + str(25 + day_of_week - day) + ")")
    ActionChains(driver).move_to_element(chart).perform()
    sleep(0.5)
    time_worked_raw = driver.find_element_by_css_selector("#bar > div").text
    time_worked = time_worked_raw[:5]
    log(time_worked)
    return time2int(time_worked)

def entered_first_time_today():
    return data['day_of_week'] != day_of_week

def json_load():
    return json.load(open(txt, 'r'))

def json_dump(txt=txt):
    json.dump(data, open(txt, 'w'))

def today_is_not_Monday():
    return day_of_week != 0

def print_time_worked_yestarday():
    print( '\n' + 'Yestarday worked: ' + int2time(worked_yestarday) )

def print_time_worked():
    print('\n\n' + 'Time worked: ' + int2time(time_worked) )

def print_time_to_work(time_to_work):
    print('\n\n' + 'Time left to work: ' + int2time(time_to_work))

def print_fun_time():
    print('\n\n' + 'Time of fun: ' + int2time(fun_time))

def print_time_to_leave():
    print('\n\n' + 'Time to leave: ' + int2time(time_to_leave))

def print_additional_time():
    print('\n\n' + 'Additional time: ' + int2time(data['additional_time']))

def print_gl_time():
	print('\n\n\n\n\n\n\n\n' + 'GL tracked time: ' + int2time(gl_time))

def process_spent_for_email(spent_for_emails):
	return 0 if len(spent_for_emails) == 0 else int(spent_for_emails)
    
data = json_load()

current_time = time2int( str(datetime.time(datetime.now()))[:5] )
time_worked = time_worked_for(today)

if not entered_first_time_today():
	time_worked = time_worked - data['fun_time'] + data['worked_from_home']
	driver.quit()
else:
	if today_is_not_Monday():
		worked_yestarday = time_worked_for(yestarday)
		driver.quit()
		spent_for_emails = input( 'Wait for dropbox to update and input time spent for emails: ' )
		spent_for_emails = process_spent_for_email(spent_for_emails)
		data = json_load()
		json_dump(txt_backup)

		data['gl_time'] += worked_yestarday
		worked_yestarday += data['worked_from_home'] - data['fun_time']
		print_time_worked_yestarday()
		data['additional_time'] += days_length - worked_yestarday
	else:
		driver.quit()
		spent_for_emails = input( 'Input time spent for emails: ' )
		spent_for_emails = process_spent_for_email(spent_for_emails)
		data['additional_time'] = 0
		worked_yestarday = days_length
		data['gl_time'] = 0

	time_worked += spent_for_emails
	data['time_of_coming'] = current_time - time_worked
	data['worked_from_home'] = 0
	data['day_of_week'] = day_of_week
	data['fun_time'] = 0
	json_dump()

time_to_work = days_length - time_worked + data['additional_time']

time_to_leave = current_time + time_to_work

fun_time = time_to_leave - data['time_of_coming'] - time_worked - time_to_work

gl_time = (day_of_week+1)*days_length - data['gl_time'] - time_worked - data['fun_time']

print_time_worked()
print_time_to_work(time_to_work)
print_fun_time()
print_time_to_leave()
print_additional_time()
print_gl_time()

add_time = input()

if len(add_time) == 0: exit()
add_time = int(add_time)

data['additional_time'] += add_time
json_dump()

time_to_work += add_time
time_to_leave += add_time

print_time_to_work(time_to_work)
print_time_to_leave()
print_additional_time()

input()
