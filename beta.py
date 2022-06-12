from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from os import path
import base64
import shutil
import requests


base_dir = path.dirname(path.realpath(__file__))
sess_data = base_dir + 'sess_data'



def get_driver():
    options = webdriver.ChromeOptions()

    # This argument will prevent from scanning qr code again and again
    # place your own username  .....\\Users\\<username>\\.....
    options.add_argument(
        f"user-data-dir={sess_data}")
    options.add_extension("extension/wa.crx")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # your need to specify the location fo chromedriver directory
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe', options=options)
    return driver

# Global variable driver
driver = get_driver()
ele_wait = 5

def open_whatsapp(wait_till=60):
    driver.get('https://web.whatsapp.com/')
    # Wait for 60sec or until page is fully loaded
    try:
        side_pane = WebDriverWait(driver, wait_till).until(
            lambda d: d.find_element(By.XPATH, '//div[@id="side"]'))
    except:
        print('Failed to open whatsapp. Try again')
        return False
    return True

def valid_user(phone_number):
    # max waiting time to find an element
    ele_wait = 5

    action = webdriver.ActionChains(driver)

    # open chat with non contact pop up
    sleep(ele_wait)
    print('\n=======================================================')
    print(f'Trying to send message to {phone_number}')
    print('Opening phone number input box')
    action.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys(
        's').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
    sleep(1)
    # Enter contact number to input box
    phone_number_box = WebDriverWait(driver, ele_wait).until(
        lambda d: d.find_element(By.XPATH, '//input[@placeholder="Phone number"]'))
    phone_number_box.clear()
    sleep(1)
    phone_number_box.send_keys(phone_number)
    print('contact number entered')
    sleep(1)
    chat_btn = WebDriverWait(driver, ele_wait).until(
        lambda d: d.find_element(By.XPATH, '//a[@class="btn-ok"]'))
    chat_btn.click()
    sleep(2)

    try:
        invalid_phone_box =  WebDriverWait(driver, ele_wait).until(
        lambda d: d.find_element(By.XPATH, '//div[@class="_3J6wB"]'))
        print(f'User with phone number {phone_number} is not on whatsapp')
        return False
    except: return True


# attatchment = path/to/attatchment/file
def send_message(phone_number, message=None, attatchment=None):
    ele_wait = 5
    action = webdriver.ActionChains(driver)
    # message_box = WebDriverWait(driver, ele_wait).until(lambda d: d.find_element_by_xpath("//div[contains(text(),'Type a message')]"))
    message_box = WebDriverWait(driver, ele_wait).until(lambda d: d.find_element(By.CLASS_NAME, 'p3_M1'))
    print(message_box)
    message_box.click()
    if not(message) and not(attatchment):
        print('No message and attatchments to send')
        return False
    
    if message and not(attatchment) :
        print('No attatchments')
        
        # Sending message
        action.send_keys(message).send_keys(Keys.ENTER).perform()
        print(f'Message Sent to {phone_number}')
    
    if not(message) and attatchment:
        print('No message provided!!!')
        # send_attatchment(attatchment)
    
    if attatchment and message:
        # Sending message
        try:
            action.send_keys(message).send_keys(Keys.ENTER).perform()
            print('Message sent')
        except:
            print("Unable to send message")
        
        # send_attatchment(attatchment)

def main(whatsapp):
    if not(open_whatsapp()):
        return 

    for user in whatsapp:
        try:
            id = user['ID']
            country_code = user['MOBILECC']
            phone_number = country_code + user['MOBILE']
            message = user['MSG']
            attatchment = base_dir + '\\test.pdf'
            if not(valid_user(phone_number)):
                continue 
            # send_message(phone_number, message, attatchment=attatchment)
            send_message(phone_number, message)
            sleep(2)
            
        except :
            print(f'Some error enocurred.')
    
    driver.quit()

whatsapp = [
    {"ID": 29, "MOBILECC": "91", "MOBILE": "321654",
        "MSG": "This is a test msg", "TEMPLATE": 1, "OTP": "ABCD", "LANG": "EN",
         },
    {"ID": 29, "MOBILECC": "91", "MOBILE": "8966891720",
        "MSG": "This is a test msg", "TEMPLATE": 2, "OTP": "ABCD", "LANG": "EN",
         },
    {"ID": 29, "MOBILECC": "91", "MOBILE": "9340952284",
        "MSG": "This is a test msg", "TEMPLATE": 2, "OTP": "ABCD", "LANG": "EN",
         }
]

tjson = {
"ReturnCode": "1",
"Whatsapp": [
{"ID":29,"MOBILECC":"91","MOBILE":"9340952284","MSG":"This is a test msg","TEMPLATE":1,"OTP":"ABCD","LANG":"EN"},
{"ID":29,"MOBILECC":"91","MOBILE":"8966891720","MSG":"This is a test msg","TEMPLATE":2,"OTP":"ABCD","LANG":"EN"}]
}

use_tjson = True

data = whatsapp
if use_tjson:
    data = tjson['Whatsapp']

main(data)  