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
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")  # fatal
driver = webdriver.Chrome('\\hpk\\cd\\chromedriver.exe', chrome_options=options)

driver.implicitly_wait(10)

driver.get('https://accounts.google.com/ServiceLogin?continue=https://www.google.com/voice&rip=1&nojavascript=1&followup=https://www.google.com/voice')

# time.sleep(10)
# doc=driver.page_source.encode('ascii', 'replace').decode('ascii')
# print(doc)
# time.sleep(300)
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

		element = driver.find_element_by_xpath("//*[contains(text(), 'Enter your password')]")
		actions = ActionChains(driver) 
		actions.move_to_element_with_offset(element, 1, 1)
		actions.send_keys(sys.argv[2])
		actions.send_keys(Keys.ENTER)
		actions.perform()
		time.sleep(1)

##		element = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
##		driver.execute_script("arguments[0].click();", element)
##		actions = ActionChains(driver) 
##		actions.move_to_element_with_offset(element, 1, 1)
##		actions.click()
##		actions.perform()

		# driver.get('https://voice.google.com/calls')

		time.sleep(1)
		doc = driver.page_source.encode('ascii', 'replace').decode('ascii')

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



id='FAIL'
for _ in range(20):
	# enter called TN
	try:
		if input_0:
			time.sleep(1)
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
	except:
		pass
	
	try:
		element = driver.find_element_by_xpath('//*[@test-id="new-call-button"]')
		driver.execute_script("arguments[0].click();", element)
	except:
		pass

	time.sleep(0.3)
	doc = driver.page_source.encode('ascii', 'replace').decode('ascii')
	p = re.search('id="(select_option_\d+)"', driver.page_source)
	if p:
		id = p.group(1)
		print("ID:",id)
		break
	else:
		print("WAITING FOR CALLING TN")
		print(driver.page_source.encode('ascii', 'replace').decode('ascii'), file=sys.stderr)

element = driver.find_element_by_id(id)
driver.execute_script("arguments[0].click();", element)

time.sleep(0.3)
element = driver.find_element_by_xpath('//button[normalize-space()="Connect"]')
driver.execute_script("arguments[0].click();", element)

time.sleep(5)
print("END")
#LOGOUT driver.get('https://accounts.google.com/SignOutOptions?hl=en&amp;continue=https://voice.google.com/u/0&amp;service=grandcentral')
#LOGOUT time.sleep(0.3)
#LOGOUT element = driver.find_element_by_id("signout")
#LOGOUT driver.execute_script("arguments[0].click();", element)

#LOGOUT time.sleep(1)

driver.close()
driver.quit()
