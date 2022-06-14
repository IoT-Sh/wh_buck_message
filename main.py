from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os, platform, time, datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfile
import secrets

URL = 'https://web.whatsapp.com/'
PATH = './chromedriver'
message = " "

driver = webdriver.Chrome(PATH)
driver.maximize_window()

USER_PATH = '//*[@class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr"]'
MSG_INPUT = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
SEND_MSG = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
search_path = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]'


def read_from_spreadsheet():
    global DATA
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    creds = service_account.Credentials.from_service_account_file('whatsappython.json',scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = secrets.SPREADSHEET_ID #replace your spreadsheet id here
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range="Sheet1").execute()

    DATA = result['values']
    print(DATA)


def send_whatsapp_message():

    global driver
    message = askstring('Message', 'Type your message here')
    while(message==" "):
        print('wait for message')
    driver.get(URL)
    print(URL)

    for i in range(len(DATA)):

        number = DATA[i][0]

        print(number)

        search_box = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, search_path)))
        search_box.send_keys(number)
        time.sleep(2)
        print("search contact")

        user = driver.find_element(by=By.XPATH, value=USER_PATH)
        user.click()
        time.sleep(1)

        input_msg = driver.find_element(by=By.XPATH, value=MSG_INPUT)
        input_msg.send_keys(message)
        time.sleep(2)

        send = driver.find_element(by=By.XPATH, value=SEND_MSG)
        send.click()
        time.sleep(2)
					

if __name__ == '__main__':
    
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    
    read_from_spreadsheet()

    # Send whatsapp message 
    send_whatsapp_message()

    # Close chromedriver
    driver.close()

