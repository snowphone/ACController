import argparse
import os
import time
import re

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


parser = argparse.ArgumentParser()
parser.add_argument("ID", help="ID of GHP WEB REMOCON")
parser.add_argument("password", help="password of GHP WEB REMOCON")

args = parser.parse_args()


def isDay():
	timestr = time.ctime()
	pattern = re.compile(r"(?<=\w{3} \w{3} \d{2} )\d{2}")
	hours = int(pattern.search(timestr).group())
	if hours in range(8, 23):
		return True
	else:
		return False




while True:
	
	'''
	opt = webdriver.ChromeOptions()
	opt.headless = True
	#opt.binary_location = "./GoogleChromePortable64/GoogleChromePortable.exe"
	browser = webdriver.Chrome(options=opt, executable_path="./chromedriver.exe")
	'''
	opt = webdriver.FirefoxOptions()
	opt.headless = True
	browser = webdriver.Firefox(options=opt, executable_path="./geckodriver.exe")

	browser.get("http://203.249.68.52")
	browser.find_element_by_id("txtId").send_keys(args.ID)

	browser.find_element_by_id("txtPwd").send_keys(args.password)
	browser.find_element_by_id("btnLogin").click()

	img_src=browser.find_element_by_id("Image_OnOff").get_attribute("src")

	#print (img_src)
	#print (img_src.find("this_1"))

	if img_src.find("this_1") == -1: 
		if isDay():
			print(time.ctime(), "AC is off. Turn on the AC")
			browser.find_element_by_id("OverImage_OnOff").click()
			browser.find_element_by_id("btnSubmit").click()
			#browser.switch_to_alert().accept()
			browser.quit()
			time.sleep(7000)
		else:
			print("It's night")
			time.sleep(3600)
	else:
		print(time.ctime(), "AC is on, sleep for 3 minutes")
		browser.quit()
		time.sleep(180)
