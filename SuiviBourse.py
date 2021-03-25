import re
import xml.etree.ElementTree as ET
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
from os import path
from datetime import date
from PIL import Image
import numpy as np
import json

import time
from collections import Counter

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
pathData = '../react-app/src/data.json'

def parseXML(file_path):
    myTree = ET.parse(file_path)
    myRoot = myTree.getroot()
    for x in myRoot:
        smsBody = x.attrib['body']
    code = re.findall(r"\d{8}", smsBody)
    os.remove(file_path)
    return code[0]


def GetAttachments(service, user_id, msg_id):
    """Get and store attachment from Message with given id.

    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param msg_id: ID of Message containing attachment.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,
                                                                       id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = part['filename']

                with open(path, 'wb') as f:
                    f.write(file_data)
        return parseXML(path)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def search_last_save(service, user_id='me'):
    lastMessage = service.users().messages().list(userId=user_id, q="subject:Sauvegarde").execute()

    return GetAttachments(service, user_id, lastMessage['messages'][0]['id'])


def connectToGmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return search_last_save(service)


"""
REFERENCE CREATION
pic_url = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAgCAIAAACZ9R/cAAAB10lEQVR42o2VPYKDIBCF35mkSRq9kbTYQLd7l03rXiDn0D5HyDaww48jMY7GqBkVmOGbx4DgfaAf3UM6fTTT0/re55fpc3ksRrwQSt/S86XJOmI9bLF4RPiN51B7iFY8KgfZrh0jNcrfPY8SOI7gx3Fsu84Yw1N7CTAEcOCLh7UF3e73+/V6UarRfS8xggSJzNvP7Xq5NI2is9daYoRdSPM8mcFQV+rcth0ZWvcSI2wgzdM8GBM9K9V17e84OmvpkSayYbSgi0ldIT3/niVypYbBPB4P+mKdoyh6YlExqnWEDaTv7y86pmlmRpaiUGki2yDKjHAqJGtTFIQzVK4qHeFUSGkIYqFZCBsdQYLE/ohFw7pYPNQ6ggSJQ3XWNTmpwmKDBImbWGdTRrS02CBBYkbEgnKstZYWGyRIzMhRFGrRRcWICUCCxC2YhVSQcFyRyHRZF5HFfkHCcUWKE0lrpE+62C1IOK5I9O9SRrIu3gvSoos9SMwor5G+ZMS/6winVduuGXlhVNXOs6qddZFZ1Iy4BU6r9lIv9IYR6wgSJB4y66Is9qo/hwkJEjPK9UKnNbK7s0GCxHMrLEidws4GCdLnOxskSKeMWEeQIJ0y4ijxyfZ/vPv/A1nAhXyQu5w7AAAAAElFTkSuQmCCWERIWUJPV1daSFVbWk9LR0FYVFZWUUtFUERZTUZTSEpFU0NUTFtRVVVRVE9SR1haWUNCUkdTVktTQ1ZMQkNLU0xFS0dVUFRVTlVQQ0RKWklQU0tGRkVWS1hNVFVDU09PRFJGQllORUpESFtLRUJMV01YUkZYRVpHTklNV0RMWktMUFFVWUFNQlRYQ0dJUEJUV1BIQ0ZFU0xRSldbU1JERFVNWVhNVEJFTEpCWktQUkhZVUhHRVZKR1RER1FXTlpNTlVPWldCSFNEWUdQWkVZVUZISVhGVlZMRU5aWFNCWEVYSVNWRFNEUUJUSFBPSkhRQlBNWlhNVkRBS0pNUUlOVEdVU0hHVUFNQlpPU0xYV1FKWFlJRUJMV0tSUE1OT0ZRTUpIWFpaVllOTkFLTUdbTVdUWEhGUVJEU0xJWUZZRUFSWUlFTVdFQkhTQ1VJV1hQS01ESUZHS1RISlpEUE1UUkZJUlZPUVpJWVBUVlhOSkpIRUVCWkJSWkpPV09HQlRJU1NLS0JDTUhJQklUWkZaRkxVSU0="
encoded_image = pic_url.encode('utf-8')

with open('./imgNumber/1.png', 'wb') as fp:
    #message_bytes = base64.b64decode(base64_bytes)

    decoded_image = base64.decodebytes(encoded_image)
    fp.write(decoded_image)
"""


# CREATE TXT REFENCE FOR IMAGE
def createExamples():
    numberArrayExamples = open('./imgNumber/numArEx.txt', 'a')
    numbersWeHave = range(0, 10)
    for eachNum in numbersWeHave:
        imgFilePath = './imgNumber/' + str(eachNum) + '.png'
        ei = Image.open(imgFilePath)
        eiar = np.array(ei)
        eiarl = str(eiar.tolist())
        lineToWrite = str(eachNum) + '::' + eiarl + '\n'
        numberArrayExamples.write(lineToWrite)


def whatNumIsThis(filePath, correspondanceNumber):
    matchedAr = []
    loadExamps = open('imgNumber/numArEx.txt', 'r').read()
    loadExamps = loadExamps.split('\n')

    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()

    inQuestion = str(iarl)

    for eachExample in loadExamps:
        try:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]

            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')

            x = 0

            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))

                x += 1
        except Exception as e:
            print(str(e))
    allMatched = Counter(matchedAr)
    mostMatched = Counter(matchedAr).most_common(10)
    print(allMatched)
    for key, tupleMatched in mostMatched:
        if key not in correspondanceNumber:
            return key

def removeNewLineAndWhiteSpace(str):
    newStr = str.strip()
    newStr = newStr.replace('\n', '')
    newStr = newStr.replace(' ', '')
    return newStr
def verifyDataAlreadyDone(today):
    if not path.exists(pathData):
        with open(pathData, 'w') as outfile:
            data = {'data': []}
            json.dump(data, outfile)
    with open(pathData) as json_file:
        data = json.load(json_file)
        for oldData in data['data']:
            if oldData['date'] == today:
                print('Les donnés journalières ont déjà été récupérés')
                sys.exit()


if not path.exists("imgNumber/numArEx.txt"):
    print('generation du fichier de reference')
    createExamples()

today = date.today()
# dd/mm/YY
today = today.strftime("%d/%m/%Y")
verifyDataAlreadyDone(today)
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
# chrome_options.add_argument('--headless')

# Using Chrome to access web
driver = webdriver.Chrome(executable_path=r'C:\chromium\chromedriver.exe', options=chrome_options)

driver.set_window_size(540, 720)
# Open the website
driver.get("https://www.caisse-epargne.fr/rhone-alpes/particuliers")

try:
    btnCookie = driver.find_element_by_id("consent_prompt_submit")
    btnCookie.click()
    time.sleep(1)
except:
    pass

styleNeuf = 'background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAgCAIAAACZ9R/cAAADFklEQVR42o2Vz2viQBTH529KNIEKFtqLdm8W4q0FhRYqKOhNYQsVFCzUe2vtRdubgoK9pbDtXvsDXFALXYjQXip0YQuJQrIvM8lzGm22assk8+bNm8/7vjfEMk3L/rKfSZ8s+pK+Z1PumL1nlvhAnNX2gz1nOescQzZwXlno0cKNYUQcn2jimum6cXd7e35+oV6pLy/PLBI3UhM3hifqwpl3huOxlkgkJFkSRFGwv/AR19fWzup1yz2H86FOCPplcf+8uQmHV2GhLElxJf59fz+RTNrubGdiIZ83dN3DiPCQRo+jYDAAxltb25PXCTLSDaPZbIi2GyGbzXkYER5SJp2GvZR43DD0RUa105pon0p8HI3mabRZuJD6/b5IT9/tduZgOEbwpygKRAKnM/H44MLNv3lxcQ5bBAKB6WyGtJERG58cn0AcsiS/TiaoI4JCKpfKEGQkGvUR0mAwZJHe3d2ijggKKZfNwQ6KEvcR0vv7X4G66PUukRHB7BxWKjAdXg2j0JcKSZJk8FGvnyEj4krbbDSbTEhvb3+4GvEKaX19DWxKpbI1z4hbC8PBkMYoHp8c+xRbJBIFF8WDA2REkBj8crksJGUlFBoOB0uLTRtrMAvnPapWkRFhVJnp09Nvqm5BlqXKYeX6+oemjUFIqnrVaDaSyQRVlg0UZIaMPtQI/Nc0bWt7m5oJgrsAiy0aiVCZi61WCxkRRzuco9ls2u10KpXD3Z1dKNDN2GY6k4HI+7/6nU4XPIKX4WCAjIh/R/I0pEIhD+tDKys8I+LfkTzFBhmFY6RSeybHmPgLiS+2+4cHRkZVVbRHXXwqJHQEgFhGNja+WVyklMXXunapXKZ9S+hd9jyMyFe6dqvdZlkuHhQXGZEPKLn1zOT+4X4vlWKqyKQzhm4sMiLYkdha6DfPL8/Q/kECuzs7TEiwvlo9WsrImmeE7npaq0FHYsUmMDGLYi6b5YW0qCPCCwn6WjAQhOTHYrF8odBut8aa9t+bjfBCmk5nS2+2RUa8jshnQvIwQiEt6oh8Boln5H/7k69c//63/z92MfBCuZhyiQAAAABJRU5ErkJgglpBUERaWEpVWlhFTkRPUkdXSE1JRENFT09XUVpQSVJaRlFDQUxZUkpUV1lSUlpMSkRNS1RCSlhKVkdSVVhFUFVPTEdWS1pZTFVESkhWSw==") center center no-repeat;'
tmpPath = os.getcwd() + "/tmp"
if not path.exists(tmpPath):
    os.mkdir(tmpPath)

isSucced = False
finalArray = {'date': today, 'dayData': {}}
time.sleep(3)
burger = driver.find_element_by_class_name("burger")
burger.click()
time.sleep(2)
btnCompte = driver.find_element_by_class_name("account-link")
btnCompte.click()
time.sleep(1)
inputId = driver.find_element_by_id("idClient")
inputId.send_keys("014123493")
inputId.submit()
try:
    ok = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "keyboard-button"))
    )
    keyboardNumber = driver.find_elements_by_class_name("keyboard-button")
    i = 0
    correspondanceNumber = []
    for number in keyboardNumber:
        i = i + 1
        style = number.get_attribute("style")
        urlPic = style.replace('background: url("data:image/png;base64,', '')
        urlPic = urlPic.replace('") center center no-repeat;', '')
        encoded_image = urlPic.encode('utf-8')
        with open('tmp/imgDecoded.png', 'wb') as fp:
            decoded_image = base64.decodebytes(encoded_image)
            fp.write(decoded_image)
        realNumber = whatNumIsThis('tmp/imgDecoded.png', correspondanceNumber)
        correspondanceNumber.append(realNumber)

    print(correspondanceNumber)

    credentialFile = open("credentials/Credentials.txt", "r")
    for number in credentialFile:
        keyboardNumber[correspondanceNumber.index(int(number))].click()

    keyboardNumber[0].submit()
    time.sleep(30)

    smsInput = driver.find_element_by_xpath(
        "//form['@class=ng-pristine ng-invalid ng-touched']/ui-input/div/input")  # /

    smsCode = connectToGmail()
    smsInput.send_keys(smsCode)
    smsInput.submit()
    time.sleep(5)
    btnCompte = driver.find_element_by_xpath("//td[text()='34332809818']")
    btnCompte.click()
    time.sleep(15)
    comptePEA = driver.find_element_by_xpath("//div[text()='13825002003433280981836 M. REMI PAPIN']")
    comptePEA.click()
    time.sleep(3)

    listArticle = driver.find_elements_by_tag_name("article")
    for article in listArticle:
        titleElement = article.find_element_by_css_selector('div.titre-bloc')
        title = titleElement.get_attribute('textContent')
        title = title.rstrip()
        finalArray['dayData'][title] = {}
        ulELement = article.find_elements_by_tag_name('ul')
        for ul in ulELement:
            liElement = article.find_elements_by_tag_name('li')
            for li in liElement:

                listSpan = li.find_elements_by_tag_name('span')
                nameValue = listSpan[0].get_attribute('textContent')
                value = listSpan[1].get_attribute('textContent')
                value = removeNewLineAndWhiteSpace(value)
                finalArray['dayData'][title][nameValue] = {}
                finalArray['dayData'][title][nameValue] = value

    with open(pathData) as json_file:
        data = json.load(json_file)

        temp = data['data']

        # python object to be appended
        y = finalArray
        # appending data to emp_details
        temp.append(y)
    with open(pathData, 'w') as outfile:
        json.dump(data, outfile)
        isSucced = True
finally:
    print(isSucced)
    print(('erreur lors de l\'ajout de données', 'Ajout des données avec succès')[isSucced])
    driver.quit()
