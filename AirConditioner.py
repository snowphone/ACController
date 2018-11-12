import asyncio
import ctypes
import multiprocessing
import os
import re
import subprocess
import threading
import time
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import *

from selenium.common.exceptions import (UnexpectedAlertPresentException,
                                        WebDriverException)
from selenium.webdriver import Chrome, ChromeOptions

from myDriver import HiddenChromeWebDriver


def isDaytime():
	timestr = time.ctime()
	pattern = re.compile(r"(?<=\w{3} \w{3} \d{2} )\d{2}")
	hours = int(pattern.search(timestr).group())
	if hours in range(8, 23):
		return True
	else:
		return False


class Browser:
	def __init__(self):
		opt = ChromeOptions()
		opt.headless = True
		#opt.binary_location = "./GoogleChromePortable64/GoogleChromePortable.exe"
		browser = HiddenChromeWebDriver(options=opt)


		self.browser = browser
		self.child = None
	
	def turn_on_once(self, identification, password):
		url = "http://203.249.68.52"
		self.browser.get(url)
		self.browser.find_element_by_id("txtId").send_keys(identification)

		self.browser.find_element_by_id("txtPwd").send_keys(password)
		self.browser.find_element_by_id("btnLogin").click()


		try:
			img_src=self.browser.find_element_by_id("Image_OnOff").get_attribute("src")
		except UnexpectedAlertPresentException:
			#-----------login failed--------------
			print("login failed")
			return None


		coldWarmCheck=self.browser.find_element_by_id("Image_1").get_attribute("src")
		if coldWarmCheck.find("nn_0") != -1:
			root.title("web remote - 난방")
		else:
			root.title("web remote - 냉방")

		turnOnSucceeded = False
		if img_src.find("this_1") == -1: 
			self.browser.find_element_by_id("OverImage_OnOff").click()
			turnOnSucceeded = True
			print("turning on the AC.", end=' ', flush=True)
		else:
			print("The AC is still running.", end=' ', flush=True)
		self.browser.find_element_by_id("btnSubmit").click()

		self.browser.get("http://203.249.68.52")
		self.browser.find_element_by_id("btnLogout").click()
		return turnOnSucceeded
	
	def turn_off(self, identification, password):
		self.browser.get("http://203.249.68.52")
		self.browser.find_element_by_id("txtId").send_keys(identification)

		self.browser.find_element_by_id("txtPwd").send_keys(password)
		self.browser.find_element_by_id("btnLogin").click()

		img_src=self.browser.find_element_by_id("Image_OnOff").get_attribute("src")

		if img_src.find("this_1") != -1: 
			self.browser.find_element_by_id("OverImage_OnOff").click()
		self.browser.find_element_by_id("btnSubmit").click()
	
	

class Redirector:
	def __init__(self, obj):
		self.obj = obj
		return
	def write(self, s):
		self.obj.insert(END, s)
		self.obj.see("end")
		#self.obj.update_idletasks()
		return
	def flush(self):
		pass
'''
main function start
'''

try:
	browser = Browser()
except:
	showerror("Critical Error", "크롬이 설치되어있는지, 교내 ip에 접속했는지 확인하세요")
	exit(1)

MARGIN=5
root = Tk(className="web remote")
root.resizable(width=False, height=False)


leftFrame = Frame(root)
leftFrame.grid(row=0)

idLabel = Label(leftFrame, text="ID")
idLabel.grid(row=0, column=0, padx=MARGIN, pady=MARGIN)

idText = StringVar()
idTextBox = Entry(leftFrame, textvariable=idText)
idTextBox.grid(row=0, column=1, padx=MARGIN, pady=MARGIN)

pwLabel = Label(leftFrame, text="Password")
pwLabel.grid(row=1, column=0, padx=MARGIN, pady=MARGIN)

pwText = StringVar()
pwTextBox = Entry(leftFrame, textvariable=pwText)
pwTextBox.grid(row=1, column=1, padx=MARGIN, pady=MARGIN)



def turn_on_closure(): 
	ret = browser.turn_on_once(idText.get(), pwText.get())
	if ret is None:
		return
	elif ret:
		sleeptimerInMin = 120
	else:
		sleeptimerInMin = 3
	print("sleep for {} minutes".format(sleeptimerInMin))
	root.after(int(sleeptimerInMin * 60 * 1000), turn_on_closure)

startButton = Button(leftFrame, text="start", command=turn_on_closure)
startButton.grid(columnspan=2, padx=MARGIN, pady=MARGIN)
pwTextBox.bind("<Return>", lambda event: turn_on_closure())
startButton.bind("<Return>", lambda event: turn_on_closure())

log = Text(root, width=50, height=10)
log.grid(row=0, column=2, padx=MARGIN, pady=MARGIN)
sys.stdout = Redirector(log)

if len(sys.argv) == 3:
	idText.set(sys.argv[1])
	pwText.set(sys.argv[2])
	turn_on_closure()


root.mainloop()
try:
	browser.turn_off(idText.get(), pwText.get())
except:
	pass
finally:
	browser.browser.quit()
