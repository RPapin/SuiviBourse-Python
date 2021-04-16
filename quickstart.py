from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Instantiate headless driver
chrome_options = Options()

# Windows path
chromedriver_location = 'chromedriver\chromedriver.exe'

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_prefs = {"download.default_directory": r"C:\Users\remip\Downloads"} # (windows)
chrome_options.experimental_options["prefs"] = chrome_prefs

driver = webdriver.Chrome(chromedriver_location,options=chrome_options)

# Download your file
driver.get('https://www.mockaroo.com/')
driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/form/div[3]/button[1]').click()