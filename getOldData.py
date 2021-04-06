import re
import pickle
import os.path
from os import path
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import base64
from datetime import date
import json
import time
from datetime import datetime

# pathData = os.path.join(os.getcwd(), 'react-app/src/data.json')
pathData = os.path.join(os.getcwd(), 'data.json')
pathBaseData = os.path.join(os.getcwd(), 'base_data.json')
today = date.today()
# dd/mm/YY
todaySlash = today.strftime("%d/%m/%Y")
todayTiret = today.strftime("%Y-%m-%d")
def getLastDatData(today):
    if not path.exists(pathData):
        with open(pathData, 'w') as outfile:
            data = {'data': []}
            json.dump(data, outfile)
        return 0
    with open(pathData) as json_file:
        data = json.load(json_file)
        for oldData in data['data']:
            if oldData['date'] == todaySlash:
                print('Les donnés journalières ont déjà été récupérés')
                sys.exit()
            else :
                mostOldDate = oldData['date']
    return mostOldDate
def dlDataFile(code, url):
    if path.exists("C:/Users/remip/Downloads/" + code + "_" + todayTiret + ".txt"):
        return True
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    # Using Chrome to access web
    driver = webdriver.Chrome(executable_path="chromedriver\chromedriver.exe", options=chrome_options)#E:\chromedriver_win32\chromedriver.exe
    driver.implicitly_wait(10)
    # Open the website
    driver.get(url)
    driver.find_element_by_id('didomi-notice-agree-button').click()
    driver.refresh()
    driver.find_element_by_xpath("/html/body/main/div/section[1]/div[2]/article/div[1]/div/div[1]/div[4]/div[2]/div[1]/div[2]/div[3]").click()
    dlBtn = driver.find_element_by_xpath("/html/body/main/div/section[1]/div[2]/article/div[1]/div/div[1]/div[4]/div[2]/div[1]/div[4]/div[4]/div")
    dlBtn.click()
    time.sleep(3)
    driver.close()
def readAndSaveData(code, date_invest, lastDayData) :
    localTable = {}
    dataFilePath = "C:/Users/remip/Downloads/" + code + "_" + todayTiret + ".txt"
    dateRegex = r"\d{2}/\d{2}/\d{4}"
    stockRegexFloat = r"\d+\.\d+"
    stockRegexInt = r"\d+"
    if path.exists(dataFilePath): 
        f = open(dataFilePath, "r")
        for line in f:
            matchesDate = re.findall(dateRegex, line)
            if len(matchesDate) > 0 :
                matchObj = datetime.strptime(matchesDate[0], '%d/%m/%Y').date()
                lastDayObj = datetime.strptime(lastDayData, '%d/%m/%Y').date()
                if matchObj > lastDayObj : #nouvelles data
                    stockmatches = re.findall(stockRegexFloat, line)
                    if len(stockmatches) == 0 :
                        stockmatches = re.findall(stockRegexInt, line)
                        localTable[matchesDate[0]] = stockmatches[len(stockmatches) - 2]
                    else : 
                        localTable[matchesDate[0]] = stockmatches[len(stockmatches) - 1]
        return localTable
def floatToEur(strfloat, isPct = False):
    eur = strfloat.replace('.', ',')
    if isPct :
        eur += '%'
    else :
        eur += '€'
    return eur
def formatData(fullData, base_data):
    days = fullData[next(iter(fullData))].keys()
    #get Existing Stock AND ADD NEW ones
    localDataTable = {}
    finalLocalTable = []
    for day in days:
        localDataTable[day] = {}
        totalStockPersonnal = 0
        for stockActionLabel in fullData.keys():
            stockValueAction = float(fullData[stockActionLabel][day])
            stockQte = base_data[stockActionLabel]['QUANTITE']
            priceBuy = base_data[stockActionLabel]['PRIX_ACHAT']
            stockValuePersonnal = round(stockValueAction*stockQte, 2)
            valuePct = round((stockValueAction - priceBuy) / priceBuy * 100, 2)
            valueEur = round((stockValueAction - priceBuy) * stockQte, 2)
            if valueEur > 0:
                latenteValue = "+" + floatToEur(str(valueEur)) + "(+" +  floatToEur(str(valuePct), True) + ")" 
            else :
                latenteValue = floatToEur(str(valueEur)) + "(" +  floatToEur(str(valuePct), True) + ")" 
            totalStockPersonnal += stockValuePersonnal

            localDataTable[day][stockActionLabel] = {
                'Titres en portefeuille' : base_data[stockActionLabel]['QUANTITE'],
                'Code ISIN' : base_data[stockActionLabel]['Code ISIN'],
                'Prix moyen' : floatToEur(str(priceBuy)),
                'Cours/VL' : floatToEur(str(stockValueAction)),
                'Valorisation' : floatToEur(str(stockValuePersonnal)),
                '+/- Values latentes' : latenteValue
                }
        
        for stockActionLabel in fullData.keys():
            actifPct = round((stockValuePersonnal / totalStockPersonnal) * 100, 2)
            localDataTable[day][stockActionLabel]['% Actif'] = actifPct
            if base_data[stockActionLabel]['LABEL'] != base_data[stockActionLabel]['CODE'] : 
                localDataTable[day][base_data[stockActionLabel]['LABEL']] = localDataTable[day][stockActionLabel]
                del localDataTable[day][stockActionLabel]

        finalLocalTable.append({"date" : day, "dayData": localDataTable[day]})  
    return finalLocalTable
def addData(formatedData):
    with open(pathData) as json_file:
        data = json.load(json_file)
        
        temp = data['data']
        # appending data to emp_details
        for dayData in formatedData:
            temp.append(dayData)
        with open(pathData, 'w') as outfile:
            json.dump(data, outfile)
            outfile.close()
        json_file.close()
def main():
    finalDataTable = {}
    lastDayData = getLastDatData(today)
    if path.exists(pathBaseData):
        with open(pathBaseData) as json_file:
            data = json.load(json_file)
            for actionDatas in data:
                dlDataFile(data[actionDatas]['CODE'], data[actionDatas]['URL'])
                finalDataTable[data[actionDatas]['CODE']] = readAndSaveData(data[actionDatas]['CODE'], data[actionDatas]['DATE_INVEST'], lastDayData)
            json_file.close()
            formatedData = formatData(finalDataTable, data)
            addData(formatedData)
            json_file.close()
        print('Done !')    
    else :
        print('No base data json')
        sys.exit()
# main()
