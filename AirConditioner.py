import argparse
import os
import datetime
import time
import re

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def isDaytime():
	hour = datetime.datetime.now().hour
	return True if hour in range(8, 23) else False

def turn_up(browser):
	increase_button=browser.find_element_by_id("OverImage_2")
	while True:
		try:
			increase_button.click()
		except UnexpectedAlertPresentException:
			browser.switch_to.alert.accept()
			return

def turn_down(browser):
	decrease_button=browser.find_element_by_id("OverImage_3")
	while True:
		try:
			decrease_button.click()
		except UnexpectedAlertPresentException:
			browser.switch_to.alert.accept()
			return

def isSummer(browser):
	coldWarmCheck=browser.find_element_by_id("Image_1").get_attribute("src")
	if coldWarmCheck.find("nn_0") != -1:
		return True
	else:
		return False

def login(browser, ID, pw):
	browser.get("http://203.249.68.52")
	browser.find_element_by_id("txtId").send_keys(args.ID)
	browser.find_element_by_id("txtPwd").send_keys(args.password)
	browser.find_element_by_id("btnLogin").click()

	return browser



def main():
	opt = webdriver.ChromeOptions()
	opt.headless = True
	browser = webdriver.Chrome(options=opt, executable_path="./chromedriver.exe")

	while True:
		login(browser, args.ID, args.password)

		img_src=browser.find_element_by_id("Image_OnOff").get_attribute("src")

		if img_src.find("this_1") == -1: 
			if isDaytime():
				if isSummer(browser):
					turn_down(browser)
				else:
					turn_up(browser)
				browser.find_element_by_id("OverImage_OnOff").click()
				browser.find_element_by_id("btnSubmit").click()
				browser.quit()
				time.sleep(7200)	# 2 hours
			else:
				time.sleep(3600 * 8.5)
		else:
			browser.quit()
			time.sleep(180)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("ID", help="ID of GHP WEB REMOCON")
	parser.add_argument("password", help="password of GHP WEB REMOCON")
	args = parser.parse_args()
	main()
