import re
import pickle
import os.path
from os import path
import glob
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import base64
from datetime import date
import json
import time
import configuration

pathToResult = r"C:\Users\remip\Documents\ACC_hive_leaderboard\result"
# JSON file
f = open('./history.json', "r")
# Reading from file
sessionHistory = json.loads(f.read())

f.close()

url = "http://TripACC:"+configuration.password+"@hive01.northeurope.cloudapp.azure.com:10001/ACC.aspx?ServerID=ACCServer80"
today = date.today()
# dd/mm/YY
todaySlash = today.strftime("%d/%m/%Y")
todayTiret = today.strftime("%Y-%m-%d")

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--use-fake-ui-for-media-stream")
# Using Chrome to access web
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
driver.implicitly_wait(5)
# Open the website
driver.get(url)

driver.find_element_by_id("HlnkResults").click()
running = True
while running:
    element = driver.find_element_by_id("DDResults")
    all_options = element.find_elements_by_tag_name("option")
    if len(sessionHistory['SessionHistory']) >= len(all_options) - 1:
        running = False
        break
    for option in all_options:
        sessionId = option.get_attribute("value")
        if sessionId not in sessionHistory['SessionHistory']:
            if sessionId != "":
                sessionHistory['SessionHistory'].append(sessionId)
                option.click()
                if len(driver.find_elements_by_id('GvResults')) > 0:
                    driver.find_element_by_id("btnResultDownload").click()
                    time.sleep(2)
                    #move result to the right folder
                    list_of_files = glob.glob(r'C:\Users\remip\Downloads\*')  # * means all if need specific format then *.csv
                    latest_file = max(list_of_files, key=os.path.getctime)
                    os.rename(latest_file, os.path.join(pathToResult, os.path.basename(latest_file)))
                    print(os.path.join(pathToResult, os.path.basename(latest_file)))
                break;
        elif sessionId != "":
            running = False
            break;

with open("history.json", "w") as outfile:
    json.dump(sessionHistory, outfile)

driver.close()

# main()
