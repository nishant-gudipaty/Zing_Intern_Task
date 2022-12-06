from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import os
import time
import zipfile
import sqlite3
import pandas as pd
from datetime import datetime, timedelta


parentFolder = r"C:\Users\Vinayak Nishant\Desktop\Projects\Zing_Intern_Task"
DRIVER_PATH = r"C:\Users\Vinayak Nishant\Desktop\Drivers\chromedriver.exe"


prefs = {
'download.default_directory': parentFolder,
'download.prompt_for_download': False,
'download.extensions_to_open': 'xml',
'safebrowsing.enabled': True
}

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',prefs)
options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--safebrowsing-disable-download-protection")
options.add_argument("safebrowsing-disable-extension-blacklist")
options.headless = True 

driver = webdriver.Chrome(options=options, executable_path = DRIVER_PATH)

os.makedirs(parentFolder + r"\bhavcopy", exist_ok = True)

# Download EQUITY.csv
driver.get("https://archives.nseindia.com/content/equities/EQUITY_L.csv")
time.sleep(2)


# Download bhavcopy
day = datetime.today() + timedelta(days=1)
strings = []; latest = False; latest_file = ""

c = 30
while c>0:
    day = day - timedelta(days=1)
    month = day.strftime("%h").upper()
    date = day.strftime("%d")
    year = day.strftime("%Y").upper()
    
    string = "cm" + date + month + year + "bhav.csv.zip"
    strings.append(string)
    url = "https://www1.nseindia.com/content/historical/EQUITIES/" + year + "//" + month + "//" + string
    print(url)
    
    driver.get(url)
    time.sleep(0.4)
    c -= 1
    
    if not latest:
        for root, dirs, files in os.walk(parentFolder):
            if string in files:
                latest = True
                latest_file = string


# Latest File
print("Latest Bhavcopy csv file",latest_file)
with open("latest.txt", 'w') as f:
    f.write(latest_file)

# Extracting files
for string in strings:
    try:
        with zipfile.ZipFile(parentFolder + f"/{string}", 'r') as zip_ref:
            zip_ref.extractall(parentFolder + "/bhavcopy")

        os.remove(parentFolder + "//" + string)
    except:
        pass

driver.quit()

