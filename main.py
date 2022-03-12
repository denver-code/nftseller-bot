import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


root = Tk()
root.geometry('500x400')
root.title("NFTs sell on OpenSea  ")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)
blacklist = [170, 34, 15, 33, 5, 1, 2, 4, 39, 3]+list(range(1, 969))
print(blacklist)
def open_chrome_profile():
	subprocess.Popen(
		[
			"start",
			"chrome",
			"--remote-debugging-port=8989",
			"--user-data-dir=" + main_directory + "/chrome_profile",
		],
		shell=True,
	)

def save_file_path():
	return os.path.join(sys.path[0], "Save_file.cloud") 

class InputField:
	def __init__(self, label, row_io, column_io, pos, master=root):
		self.master = master
		self.input_field = Entry(self.master)
		self.input_field.label = Label(master, text=label)
		self.input_field.label.grid(row=row_io, column=column_io)
		self.input_field.grid(row=row_io, column=column_io + 1)
		try:
			with open(save_file_path(), "rb") as infile:
				new_dict = pickle.load(infile)
				self.insert_text(new_dict[pos])
		except FileNotFoundError:
			pass

	def insert_text(self, text):
		self.input_field.delete(0, "end")
		self.input_field.insert(0, text)

	def save_inputs(self, pos):
		input_save_list.insert(pos, self.input_field.get())
		with open(save_file_path(), "wb") as outfile:
			pickle.dump(input_save_list, outfile)

###input objects###
start_num_input = InputField("Start Number:", 3, 0, 0)
end_num_input = InputField("End Number:", 4, 0, 1)
price = InputField("Price:", 5, 0, 2)
hash_link = InputField("Hash:", 6, 0, 3)


###save inputs###
def save():
	start_num_input.save_inputs(0)
	end_num_input.save_inputs(1)
	price.save_inputs(2)
	hash_link.save_inputs(3)
   

# _____MAIN_CODE_____
def main_program_loop():
	###START###
	project_path = main_directory
	start_num = int(start_num_input.input_field.get())
	end_num = int(end_num_input.input_field.get())
	loop_price = float(price.input_field.get())
	loop_hash_link = str(hash_link.input_field.get())

	##chromeoptions
	opt = Options()
	opt.add_experimental_option("debuggerAddress", "localhost:8989")
	driver = webdriver.Chrome(
		executable_path=project_path + "/chromedriver.exe",
		chrome_options=opt,
	)
	wait = WebDriverWait(driver, 60)

	###wait for methods
	def wait_css_selector(code):
		wait.until(
			ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
		)
		
	def wait_css_selectorTest(code):
		wait.until(
			ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
		)    

	def wait_xpath(code):
		wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

	

	while end_num >= start_num:
		if start_num not in blacklist:
			driver.get(f"https://opensea.io/assets/matic/{loop_hash_link}/{start_num}/sell")
			price_input = driver.find_element_by_name("price")
			price_input.send_keys("0.03")

			duration_dropdown = driver.find_element_by_id("duration")
			duration_dropdown.click()

			date_picker = driver.find_element_by_xpath("//input[@type='date' and @value='2022-03-11']")

			date_picker.click()
			date_picker.send_keys("03")
			date_picker.send_keys(Keys.ARROW_RIGHT)
			date_picker.send_keys("09")
			price_input.click()

			complete_listing = driver.find_element_by_xpath("//button[@type='submit']")
			complete_listing.click()

			wait_xpath('//*[@id="Body react-aria-2"]/div/div/button')
			sign = driver.find_element_by_xpath('//*[@id="Body react-aria-2"]/div/div/button')
			sign.click()

			time.sleep(1)

			main_page = driver.current_window_handle
			for handle in driver.window_handles:
				print(handle)
				if handle != main_page:
					login_page = handle

			driver.switch_to.window(login_page)
			wait_css_selector("button[data-testid='request-signature__sign']")
			sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
			sign.click()
			
			# change control to main page
			driver.switch_to.window(main_page)
			time.sleep(3)

		start_num += 1
		print(f'NFT {start_num-1} selled!')

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)

open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)

try:
	with open(save_file_path(), "rb") as infile:
		new_dict = pickle.load(infile)
		global upload_path
		upload_path = new_dict[0]
except FileNotFoundError:
	pass
#####BUTTON ZONE END#######
root.mainloop()