from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
import threading
import requests
import json

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=./User_data')

driver = webdriver.Chrome("./chromedriver",chrome_options=options) 
# driver = webdriver.Chrome("./chromedriver")
driver.get("https://web.whatsapp.com/") 
wait = WebDriverWait(driver, 500) 

bot_users = {}
while True:
	string = "Message sent!!!" 

	unread = driver.find_elements_by_class_name("OUeyt")
	print("Total unread :"+ str(len(unread)))
	for msgs in unread:
		action = webdriver.common.action_chains.ActionChains(driver)	
		# print("bv")
		action.move_to_element_with_offset(msgs, 0, -20)
		# print("cd")
		action.click()
		action.perform()
		action.click()
		action.perform()
		# print("ef")
		name,message = '',''
		name = driver.find_element_by_class_name("_25Ooe").text
		# print(name)
		message = driver.find_elements_by_class_name("vW7d1")[-1]
		image = message.find_elements_by_class_name("_3v3PK")
		if 'activate bot' in message.text.lower():
			if name not in bot_users:
				bot_users[name] = True
				text_box = driver.find_element_by_class_name("_2S1VP")
				response = "HI" + name
				text_box.send_keys(response + Keys.ENTER)
		if name in bot_users:
			if len(image)!=0:
				print(image)

			print(bot_users)

			complete_message = message.text.split('\n')
			print(complete_message[0])
			query = complete_message[0]
			endpoint = "https://api.dialogflow.com/v1/query?v=20150910"
			headers = {"Authorization":"Bearer c81b88ee80f64e8382fe97a7714c5bad"}
			abc = {
					"lang": "en",
					"query": query,
					"sessionId": "A12345",
					"timezone": "America/New_York"
				}
			r =requests.request('POST',endpoint,headers = headers, json =abc)
			answer = r.json()
			if answer["status"]["code"]!=401:
				queryresponse = json.dumps(answer["result"]["fulfillment"]["speech"])
				call = json.dumps(answer["result"]["actionIncomplete"])
			else:
				queryresponse = "Error"
			
			inp_xpath = '//div[@dir="ltr"][@data-tab="1"][@spellcheck="true"]'
			input_box = wait.until(EC.visibility_of_element_located(( 
				By.XPATH, inp_xpath)))
			input_box.send_keys(queryresponse + Keys.ENTER)
			time.sleep(5)
		# print(complete_message[1])