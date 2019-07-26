import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # remove this line if you want to see the browser popup
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')
options.add_argument("user-data-dir=/hpk/cd/selenium") 
driver = webdriver.Chrome('\\hpk\\cd\\chromedriver.exe', chrome_options=options)


driver.get('https://accounts.google.com/ServiceLogin?continue=https://www.google.com/voice&rip=1&nojavascript=1&followup=https://www.google.com/voice')

input_0 = False

for _ in range(30):
	time.sleep(0.5)
	doc=driver.page_source.encode('ascii', 'replace').decode('ascii')

	p = re.search('Sign in to continue to Google Voice|Sign in with your Google Account', doc)
	if p:
		print("LOGIN")
		driver.find_element_by_id('Email').send_keys(sys.argv[1])
		driver.find_element_by_id('next').click()
		time.sleep(1)
		driver.find_element_by_id('Passwd').send_keys(sys.argv[2])
		driver.find_element_by_id('signIn').click()
		# driver.get('https://voice.google.com/calls')

	p = re.search('Make a call.*? class="([^ ]*)', doc)
	if p:
		print("MAKE A CALL", p.group(1))
		# element = driver.find_elements_by_class_name('md-body-1')[1]
		time.sleep(1)
		element = driver.find_element_by_class_name(p.group(1))
		driver.execute_script("arguments[0].click();", element)
		break

	p = re.search('id="input_0"', doc)
	if p:
		print("INPUT_0")
		input_0 = True;
		break



# enter called TN
if input_0:
	driver.find_element_by_id('input_0').send_keys(sys.argv[3])
	actions = ActionChains(driver) 
	actions.send_keys(Keys.ENTER)
	actions.perform()
else:
	time.sleep(1)
	actions = ActionChains(driver) 
	actions.send_keys(sys.argv[3])
	actions.send_keys(Keys.ENTER)
	actions.perform()


id='FAIL'
for _ in range(20):
	time.sleep(0.3)
	doc = driver.page_source.encode('ascii', 'replace').decode('ascii')
	p = re.search('id="(select_option_\d+)"', driver.page_source)
	if p:
		id = p.group(1)
		print("ID:",id)
		break
	else:
		print("WAITING FOR CALLING TN")

element = driver.find_element_by_id(id)
driver.execute_script("arguments[0].click();", element)

time.sleep(0.3)
element = driver.find_element_by_xpath('//button[normalize-space()="Connect"]')
driver.execute_script("arguments[0].click();", element)

time.sleep(5)
print("END")

driver.close()
driver.quit()
