from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import date, datetime
from os import name, path, times
import base64
import shutil
import requests
from testSheetApi import get_contacts, update_sheet

base_dir = path.dirname(path.realpath(__file__))
sess_data = base_dir + 'sess_data'


def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %I:%M:%S%p")    
    return timestamp

tjson = {
    "ReturnCode":
    "1",
    "Whatsapp": [{
        "ID": 29,
        "MOBILECC": "65",
        "MOBILE": "80001235",
        "MSG": "This is a test msg",
        "TEMPLATE": 1,
        "OTP": "ABCD",
        "LANG": "EN"
    }, {
        "ID": 29,
        "MOBILECC": "65",
        "MOBILE": "82220000",
        "MSG": "This is a test msg",
        "TEMPLATE": 2,
        "OTP": "ABCD",
        "LANG": "EN"
    }]
}


def create_img(string):
    with open('images/img.png', 'wb') as f:
        img = base64.b64decode(string)
        f.write(img)


# url = 'http://example.com/img.png'
def get_img(url):
    name = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(f'images/{name}', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_driver():
    options = webdriver.ChromeOptions()

    # This argument will prevent from scanning qr code again and again
    # place your own username  .....\\Users\\<username>\\.....
    options.add_argument(f"user-data-dir={sess_data}")
    # options.add_extension("extension/wa.crx")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # your need to specify the location fo chromedriver directory
    driver = webdriver.Chrome(executable_path='chromedriver.exe',
                              options=options)
    return driver


# Global variable driver
driver = get_driver()
ele_wait = 5


def open_whatsapp(wait_till=60):
    # Wait for 60sec or until page is fully loaded
  
    driver.get('https://web.whatsapp.com/')
    try:
        side_pane = WebDriverWait(driver, wait_till).until(
            lambda d: d.find_element(By.XPATH, '//div[@id="side"]'))
    except:
        print('Failed to open whatsapp. Try again')
        return False
    print("Whatsapp opened sucessfully")
    return True


def valid_user(phone_number):
    print("valid user called")
    # max waiting time to find an element
    ele_wait = 5

    action = webdriver.ActionChains(driver)

    # open chat with non contact pop up
    sleep(ele_wait)
    print('=======================================================')
    print(f'Trying to send message to {phone_number}')
    print('Opening phone number input box')
    new_chat_btn =WebDriverWait(
        driver, ele_wait).until(lambda d: d.find_element(
            By.XPATH, '//div[@id="startNonContactChat"]'))
    new_chat_btn.click()
    sleep(1)
    # Enter contact number to input box
    phone_number_box = WebDriverWait(
        driver, ele_wait).until(lambda d: d.find_element(
            By.XPATH, '//input[@placeholder="Phone number"]'))
    phone_number_box.clear()
    phone_number_box.send_keys(phone_number)
    print('contact number entered')
    chat_btn = WebDriverWait(driver, ele_wait).until(
        lambda d: d.find_element(By.XPATH, '//a[@class="btn-ok"]'))
    chat_btn.click()
    sleep(5)

    try:
        invalid_phone_box = WebDriverWait(driver, 2).until(
            lambda d: d.find_element(By.XPATH, '//div[@data-animate-modal-popup="true"]'))
        print(f'User with phone number {phone_number} is not on whatsapp')
        invalid_phone_box_okay_btn = invalid_phone_box.find_element(By.XPATH, '//div[@role="button"]')
        invalid_phone_box_okay_btn.click()

        return False
    except:
        return True


def send_attatchment(attatchment):

    attatchment_box = WebDriverWait(driver, ele_wait).until(
        lambda d: d.find_element(By.XPATH, '//div[@title="Attach"]'))
    attatchment_box.click()
    sleep(1)

    image_box = WebDriverWait(driver, ele_wait).until(lambda d: d.find_element(
        By.XPATH,
        '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
    # attatchment = input('Enter the path of file: ')
    try:
        image_box.send_keys(attatchment)
        sleep(2)
        send_btn = WebDriverWait(driver, ele_wait).until(
            lambda d: d.find_element(By.XPATH, '//span[@data-testid="send"]'))
        sleep(2)
        send_btn.click()
        print(f'Attatchment sent  ')
        # Attatchment sent
    except:
        print('Unable to send attatchment')


def message_attatchment(message, attatchment):
    ele_wait = 5
    action = webdriver.ActionChains(driver)

    message_box = WebDriverWait(
        driver,
        ele_wait).until(lambda d: d.find_element(By.CLASS_NAME, 'p3_M1'))
    message_box.click()

    action.send_keys(message).perform()
    send_attatchment(attatchment)


# attatchment = path/to/attatchment/file
def send_message(phone_number, message=None, attatchment=None):
    ele_wait = 5
    action = webdriver.ActionChains(driver)
    message_box = WebDriverWait(
        driver,
        ele_wait).until(lambda d: d.find_element(By.CLASS_NAME, 'p3_M1'))
    message_box.click()
    if not(message) and not(attatchment):
        print('No message and attatchments to send')
        return False

    elif message and not (attatchment):
        print('No attatchments')

        # Sending message
        action.send_keys(message).send_keys(Keys.ENTER).perform()
        print(f'Message Sent to {phone_number}')

    elif not (message) and attatchment:
        print('No message provided!!!')
        send_attatchment(attatchment)

    elif attatchment and message:
        message_attatchment(message, attatchment)

    sleep(2)




def main(data):
    if not (open_whatsapp()): return
    users = []
    try:
        for ind, d in enumerate(data):
            user = d
            name = user[0]
            country_code = '91'
            phone_number = country_code + str(user[1])
            message = user[2]
            status = user[3]
            timestamp = user[4]
            attatchment = user[5]
            if attatchment:
                attatchment = base_dir + f'\\images\\{attatchment}'

            print(f'{ind}. Sending message to {name}')
            
            if status:
                
                print(f'Message is already sent to {name} at {timestamp}')
            
            elif not (valid_user(phone_number)):   
                user[3] = 'Invalid User'
                pass
            else:
                send_message(phone_number, message, attatchment=attatchment)
                # send_message(phone_number, message)
                cur_timestamp = get_timestamp()
                user[3] = 'Sent'
                user[4] = cur_timestamp
    
            users.append(user)
    
        # print(f'Some error enocurred. Possible key not found error')
        print('=======================================================')
        print('')
    finally:
        print(users)
        update_sheet(users)
    # driver.quit()



data = get_contacts()
print(data)
main(data)
