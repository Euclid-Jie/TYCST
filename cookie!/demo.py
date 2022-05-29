from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
import pickle
import os
import time

def get_cookie_from_network():

 url = 'https://www.tianyancha.com/search?key=9144030072713064X7'
 driver = Chrome()
 driver.get(url)

 # 获得 cookie信息
 time.sleep(3)
 cookie_list = driver.get_cookies()
 #print(cookie_list)
 cookie_dict = []
 for cookie in cookie_list:
  if 'name' in  cookie and 'value' in cookie:
   cookie_dict.append(cookie['name'] +'='+ cookie['value'])
 return cookie_dict


list = get_cookie_from_network()
print(';'.join(list))