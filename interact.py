from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
import os

def run_user(host, user):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    options.binary_location = "/usr/bin/google-chrome-stable"

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
    
    driver.get(f"{host}/#/login") 
    email = driver.find_element('id', 'email')
    email.send_keys(users[user]["username"])
    
    password = driver.find_element('id', 'password')
    password.send_keys(users[user]["password"])
    
    submit = driver.find_element(By.XPATH, '//button[text()="Sign In"]')
    submit.click()

    driver.get(f"{host}/#/profile")
    time.sleep(1)
    
    driver.get(f"{host}/#/admin/userlist")
    time.sleep(1)
    
    driver.get(f"{host}/#/admin/productlist")
    time.sleep(1)
    
    driver.get(f"{host}/#/admin/orderlist")
    time.sleep(1)
    
    num_products = 16
    
    for i in range(1, num_products):
       driver.get(f"{host}/#/product/{i}")
       
    driver.quit()
    
    return

host = os.environ.get('APP_HOST')
users = {
    "shoppe_admin": {
        "username":"shoppe_admin@noirusa.net",
        "password":"uR45@twDoSCa2rT814H#"
    },
}

for user in users:
    run_user(host, user)

