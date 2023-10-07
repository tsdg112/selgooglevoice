import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options, executable_path=r'C:\hpk\cd\geckodriver.exe')
driver.set_window_size(1024, 768)

driver.implicitly_wait(1)

driver.get('https://accounts.google.com/ServiceLogin?continue=https://www.google.com/voice&rip=1&nojavascript=1&followup=https://www.google.com/voice')
input_0 = False

for _ in range(30):
	time.sleep(0.5)
	try:
		driver.find_element_by_id('il1')
		break
	except:
		pass

	doc=driver.page_source.encode('ascii', 'replace').decode('ascii')
	p = re.search('Sign in to continue to Google Voice|Sign in with your Google Account', doc)
	if p:
		driver.find_element_by_id('Email').send_keys(sys.argv[1])
		driver.find_element_by_id('next').click()
		time.sleep(1)

		element = driver.find_element_by_xpath("//*[contains(text(), 'Enter your password')]")
		actions = ActionChains(driver) 
		actions.move_to_element_with_offset(element, 1, 1)
		actions.send_keys(sys.argv[2])
		actions.send_keys(Keys.ENTER)
		actions.perform()
		time.sleep(2)

		doc = driver.page_source.encode('ascii', 'replace').decode('ascii')

	p = re.search('Make a call.*? class="([^ ]*)', doc)
	if p:
		print("MAKE A CALL", p.group(1))
		time.sleep(1)
		element = driver.find_element_by_class_name(p.group(1))
		driver.execute_script("arguments[0].click();", element)
		break

	p = re.search('id="input_0"', doc)
	if p:
		print("INPUT_0")
		input_0 = True;
		break


driver.implicitly_wait(10)
try:
	driver.find_element_by_id('il1').send_keys(sys.argv[3])
except:
	print("GATE1")
	print(driver.page_source.encode('ascii', 'replace').decode('ascii'))
	driver.close()
	driver.quit()
	sys.exit()
	
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@gv-test-id="new-call-button"]').click()
element = driver.find_element_by_xpath('//*[@role="listbox"]')
driver.execute_script("arguments[0].click();", element)
element = driver.find_element_by_xpath('//*[@role="option"]')
driver.execute_script("arguments[0].click();", element)
actions = ActionChains(driver) 
actions.move_to_element_with_offset(element, 6, 6)
actions.click()
actions.perform()
element = driver.find_element_by_xpath("//*[contains(text(), 'Connect')]")
driver.execute_script("arguments[0].click();", element)

time.sleep(0.3)
try:
	element = driver.find_element_by_xpath('//button[normalize-space()="Connect"]')
	driver.execute_script("arguments[0].click();", element)
except:
	pass

time.sleep(5)

driver.close()
driver.quit()
