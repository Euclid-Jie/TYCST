import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd
import numpy as np
from retrying import retry

import os
import time
import tqdm

def get_new_cookie_from_network():

 print('<-重新获取cookie....')

 url = 'https://www.tianyancha.com/search?key=9144030072713064X7'

 option = ChromeOptions()
 option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    
 s = Service(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
 driver = Chrome(service=s,options=option) #模拟开浏览器
 driver.get(url)

 # 获得 cookie信息
 time.sleep(3)
 cookie_list = driver.get_cookies()

 driver.quit()

 cookie_dict = []
 for cookie in cookie_list:
    if 'name' in  cookie and 'value' in cookie:
        cookie_dict.append(cookie['name'] +'='+ cookie['value'])
    
 new_cookie = ';'.join(cookie_dict)
 print('cookie更新完毕!!!')
 return new_cookie

#定义一个根据网址,返回soup格式的函数
def get_URL(URL,my_cookie):
    headers = {'cookie':my_cookie,'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
    response = requests.get(URL,headers=headers) #获取网页源码
    response.encoding = 'utf-8' #设置编码格式
    html = response.text #转换格式为html
    soup = BeautifulSoup(html,features="lxml") #转换为soup格式，方便下文处理
    return(soup)

#根据公司名返回发票头数据
@retry(stop_max_attempt_number = 3)
def get_taxdata (company_name):
    #print(f'开始获取{company_name}数据')
    #company_name = '光大控股创业投资（深圳）有限公司'
    #使用天眼查平台，企查查封ip
    URL = 'https://www.tianyancha.com/search?key='+company_name
    
    global my_cookie
    
    try:
        company_list = get_URL(URL,my_cookie)
        #print(company_list)
        list = company_list.find('div',"result-list sv-search-container")
        company = list.find('div')
        title = company.find('a')
        company_url = title.get('href') #获得公司网址
    except:
        my_cookie = get_new_cookie_from_network()
        company_list = get_URL(URL,my_cookie)
        #print(company_list)
        list = company_list.find('div',"result-list sv-search-container")
        company = list.find('div')
        title = company.find('a')
        company_url = title.get('href') #获得公司网址
    
    url_head = 'https://www.tianyancha.com/cloud-wechat/qrcode.json?gid='
    response = requests.get(url_head+company_url.split('/')[-1]) #获取网页源码
    response.encoding = 'utf-8' #设置编码格式
    #print(response)
    html = response.text #转换格式为html
    #print(html)

    data_list = []
    try:
        for item in html.split(',')[4:10]:
            a = item.split(':')[1].strip('"')
            data_list.append(a)
        
    except:
        data_list = []
        for item in html.split(',')[4:11]:
            try:
                a = item.split(':')[1].strip('"')
                data_list.append(a)
            except:    
                a = item.split(':')[0].strip('"')
        data_list[-1]

    return data_list



## 正式运行
print('请输入开始位置:')
start = input()
print('请输入结束位置:')
end = input()

start_time = time.perf_counter()

df = pd.read_excel(r'C:\Users\欧玮杰\Desktop\我和我所热爱的\python\爬企查查税头\123.xls') #读取文件为df
#添加空列
cols = ['企业名称','企业税号','企业地址','企业电话','开户银行','银行账户']
for item in cols:
    df[item] = np.nan
try:
    for i in range(int(start)-1,int(end)):
        if i % 10 == 0:
            print(f"开始执行第{i+1}项任务")

        company_name = df['公司名'][i]
        data_list = get_taxdata (company_name)
        df.loc[i,'企业名称':'银行账户'] = data_list
    
    finish = time.perf_counter()
    print(f"->全部任务结束，耗时{round(finish - start_time,2)}秒")
    df.to_csv(str(start)+'_'+str(end)+'.csv',index=False)
except:
    finish = time.perf_counter()
    print(f"->任务异常结束，耗时{round(finish - start_time,2)}秒")
    df.to_csv(str(start)+'_'+str(end)+'.csv',index=False)
