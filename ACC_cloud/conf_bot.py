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

url = "https://teams.microsoft.com/l/meetup-join/19%3ameeting_YzMzZDRjOGItYWJkYy00NmY2LTkxMDItMDYwYzU0ZmU5YjAx%40thread.v2/0?context=%7b%22Tid%22%3a%227cff8eaa-92a3-41a5-92ce-6220d13f9cea%22%2c%22Oid%22%3a%225740b2b7-9de3-4ab9-bbca-e82afa7102b1%22%2c%22IsBroadcastMeeting%22%3atrue%7d&btype=a&role=a"

def connect(username):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--disable-notifications")

    # Using Chrome to access web
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.implicitly_wait(5)
    # Open the website
    driver.get(url)
    element = driver.find_element_by_id('teamsLauncher')
    element.send_keys()
    # driver.send_keys
    time.sleep(1000)

    # driver.close()
connect('aa')
# main()
