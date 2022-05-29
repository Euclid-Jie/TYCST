import time
import threading
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

# 用于选取文件路径
def getLocalFile():
    root=tk.Tk()
    root.withdraw()
    filePath=filedialog.askopenfilename()
    return filePath

#定义一个根据网址，返回soup格式的函数，因为后文多次用到，所以写成函数
def get_URL(URL):
    headers = {'cookie':'qcc_did=0f41880e-c5c1-47a7-a869-cb1cb0f6cfff; UM_distinctid=1801638b9ea18f-060c7d35fcc0e6-1a343370-e1000-1801638b9ebc6b; QCCSESSID=b94f5af24d88d0456e233a5d18; zg_5068e513cb8449879f83e2a7142b20a6=%7B%22sid%22%3A%201650452721026%2C%22updated%22%3A%201650452721026%2C%22info%22%3A%201650452721029%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%8B%9B%E6%8A%95%E6%A0%87WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%7D; zg_did=%7B%22did%22%3A%20%2218046a5ed7da48-08765c1ea21e0d-6b3e555b-e1000-18046a5ed7ec1b%22%7D; zg_d609f98c92d24be8b23d93a3e4b117bc=%7B%22sid%22%3A%201650706179886%2C%22updated%22%3A%201650706194849%2C%22info%22%3A%201650706179889%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%7D; SECKEY_ABVK=FDZVW3g8oQEnc/GT8AunVnFchqqIP6cY6sjdOcFoKxU%3D; BMAP_SECKEY=qSwC5U-XiBhLK4fO8e6XSUp9qlKbe1oIySuA9dNT28IZtUtx7MWzy3dUKJCan9UgIxqHecnuNbtHFZcNPIG7Y8lyYv5g3oupZaaWk1L4KqNnnvp9XQ7DkPS5LfSqwXr7c574FhyUstn1C1WfoJ76X7LBoXcNlxwvZG8rIu1VVDu_c7J_ZtOpR7FpW1wU01us; acw_tc=24aa139816511975366921344ef7324844f683e28521e30c94819f04ca; CNZZDATA1254842228=1870928680-1649630817-https%253A%252F%252Fcn.bing.com%252F%7C1651196066',\
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' }
    response = requests.get(URL,headers=headers) #获取网页源码
    response.encoding = 'utf-8' #设置编码格式
    html = response.text #转换格式为html
    soup = BeautifulSoup(html,features="lxml") #转换为soup格式，方便下文处理
    return(soup)

#根据公司名返回发票头数据
def get_taxdata (company_name,num):
    global result
    print(f"-> 线程{num} 启动")
    #company_name = '光大控股创业投资（深圳）有限公司'
    #使用天眼查平台，企查查封ip
    URL = 'https://www.tianyancha.com/search?key='+company_name
    company_list = get_URL(URL)
    #list = company_list.find('div',"result-list sv-search-container")
    #company = list.find('div')
    title = company_list.find('a','name select-none')
    company_url = title.get('href') #获得公司网址

    option = ChromeOptions()
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = Chrome(options=option)

    driver.get(company_url) #载入公司网址
    #模拟点击发票抬头
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR,'#company_web_top > div.footer > div.link-hover-click.focusBtn.fptt-content > span:nth-child(2)').click()
    #获得发票抬头信息
    sleep(0.5)
    a = driver.find_element(By.CLASS_NAME,'invoice-left ')
    text = a.get_attribute('outerHTML')
    driver.quit() #关闭浏览器

    #数据处理
    soup = BeautifulSoup(text,features="lxml")
    temp_list = soup.div.findAll('div')
    data_list = [] #用于存储数据
    for item in temp_list:
        data_list.append(item.span.get_text())
    
    #print(data_list)
    result.append(data_list)
    print(f"-> 线程{num} 结束")


## 正式运行
path = getLocalFile() #获取文件路径
df = pd.read_excel(path) #读取文件为df
#添加空列
cols = ['企业名称','企业税号','企业地址','企业电话','开户银行','银行账户']
for item in cols:
    df[item] = np.nan

start = time.perf_counter()

thread_list = []
result = []

for i in range(0,6):
    company_name = df['公司名'][i]
    thread = threading.Thread(target = get_taxdata , args=[company_name,i+1])
    thread.start()
    thread_list.append(thread)
    
for t in thread_list:
    t.join()

finish = time.perf_counter()

print(f"->全部任务结束，耗时{round(finish - start,2)}秒")
print(result)