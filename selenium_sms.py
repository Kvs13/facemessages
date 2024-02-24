from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
def send_message(name,number):
    driver_path = '/Users/smenliev/Library/Google/chromedriver_mac_arm64/chromedriver'
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument(f"executable_path={driver_path}")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("http://localhost:8000")

    hour_input = driver.find_element('id',"timeInput")
    phone_input = driver.find_element('id',"phone")
    submit_button = driver.find_element("tag name", "button")


    hour_input.send_keys(name)
    phone_input.send_keys(number)

    # time.sleep(2)

    submit_button.click()

