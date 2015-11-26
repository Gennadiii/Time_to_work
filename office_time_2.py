from datetime import datetime
import json
from selenium import webdriver
from os.path import expanduser

def time2int(time):
	return int( time[:2] )*60 + int( time[3:] )
def int2time(integer):
	return str(integer // 60) + ':' + '0'*(integer % 60 < 10) + str(integer % 60)

txt = expanduser(r'~\Dropbox\Work\Python\Programms\txt\office_time_2.txt')
current_time_int = time2int( str(datetime.time(datetime.now()))[:5] )

driver = webdriver.Chrome(expanduser(r'~\Dropbox\Work\Python\chromedriver.exe'))
driver.get('https://portal-ua.globallogic.com/officetime/')
driver.implicitly_wait(600)

table_view = driver.find_element_by_xpath("//a[contains(text(), 'Table view')]")
table_view.click()

today = str(datetime.now().day) + '.' + str(datetime.now().month) + '.' + str(datetime.now().year)
yestarday = str(datetime.now().day-1) + '.' + str(datetime.now().month) + '.' + str(datetime.now().year)

def time_worked_for(day):
	time_worked = driver.find_elements_by_xpath("//div[@data-day='" + day + "']")
	time_worked = time_worked[1].text
	no_teleport_int = time2int( time_worked[ time_worked.find(':')-2 : time_worked.find(':')+3 ] )
	time_worked = time_worked[ time_worked.find(':')+1 : ]
	teleport_int = time2int( time_worked[ time_worked.find(':')-2 : time_worked.find(':')+3 ] )
	return no_teleport_int + teleport_int

time_worked = time_worked_for(today)
time_of_coming = current_time_int - time_worked

data = json.load(open(txt, 'r'))

if data['today'] != today:
	last_additional_time = data['additional_time']
	additional_time = last_additional_time + ( 8*60 - time_worked_for(yestarday) )
	if additional_time < 0: additional_time = 0
	data = { 'today':today, 'time_of_coming':time_of_coming, 'additional_time':additional_time }
	json.dump(data, open(txt, 'w'))

driver.quit()

data = json.load(open(txt, 'r'))

time_of_coming = data['time_of_coming']
additional_time = data['additional_time']

time_to_work_int = 8*60 - time_worked + additional_time
time_to_work = int2time(time_to_work_int)

time_to_leave_int = current_time_int + time_to_work_int
time_to_leave = int2time(time_to_leave_int)

fun_time_int = time_to_leave_int - time_of_coming - time_worked - time_to_work_int
fun_time = int2time(fun_time_int)

print('\n\n' + 'Time left to work: ' + time_to_work)
print('\n\n' + 'Time of fun: ' + fun_time)
print('\n\n' + 'Time to leave: ' + time_to_leave + '\n\n')
if additional_time != 0: print( '\n\n' + 'Additional_time : ' + str(additional_time) )
input()
