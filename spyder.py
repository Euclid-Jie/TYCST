import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome,ChromeOptions
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
    headers = {'cookie':'_gat_gtag_UA_123487620_1=1;Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1651335834;refresh_page=0;acw_tc=781bad4416513358330697486e3209224d1b0ccc563371e18ac0ca4c8b2c60;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221807b4926c756c-0ff6a03232d57d-12333272-921600-1807b4926c85f4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%221807b4926c756c-0ff6a03232d57d-12333272-921600-1807b4926c85f4%22%7D;sajssdk_2015_cross_new_user=1;ssuid=8362546006;TYCID=ed08a7a0c8a111ecaa4b4f2a5d5c0a9d;bannerFlag=true;csrfToken=l2R-mKbX5d7Ssrx8E6p8T4-O;_gid=GA1.2.398529121.1651335834;acw_sc__v2=626d6299ba1d31e05ddd8665006220e297a9cf83;Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1651335834;_ga=GA1.2.1938865398.1651335834;aliyungf_tc=0906d9ffa882bee77e555ebd640d2df27492d6dc20d0f04b492966721414f98d',\
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' }
    response = requests.get(URL,headers=headers) #获取网页源码
    response.encoding = 'utf-8' #设置编码格式
    html = response.text #转换格式为html
    soup = BeautifulSoup(html,features="lxml") #转换为soup格式，方便下文处理
    return(soup)

#根据公司名返回发票头数据
def get_taxdata (company_name):
    #company_name = '光大控股创业投资（深圳）有限公司'
    #使用天眼查平台，企查查封ip
    URL = 'https://www.tianyancha.com/search?key='+company_name
    company_list = get_URL(URL)
    #list = company_list.find('div',"result-list sv-search-container")
    #company = list.find('div')
    title = company_list.find('a','name select-none')
    company_url = title.get('href') #获得公司网址

    driver = Chrome() #模拟开浏览器
    driver.get(company_url) #载入公司网址
    #模拟点击发票抬头
    sleep(1)
    driver.find_element_by_css_selector('#company_web_top > div.footer > div.link-hover-click.focusBtn.fptt-content > span:nth-child(2)').click()
    #获得发票抬头信息
    sleep(1)
    a = driver.find_element_by_class_name('invoice-left ')
    text = a.get_attribute('outerHTML')
    driver.quit() #关闭浏览器

    #数据处理
    soup = BeautifulSoup(text,features="lxml")
    temp_list = soup.div.findAll('div')
    data_list = [] #用于存储数据
    for item in temp_list:
        data_list.append(item.span.get_text())
    
    return data_list



## 正式运行
path = getLocalFile() #获取文件路径
df = pd.read_excel(path) #读取文件为df
#添加空列
cols = ['企业名称','企业税号','企业地址','企业电话','开户银行','银行账户']
for item in cols:
    df[item] = np.nan

try:
    for i in range(0,10):
        company_name = df['公司名'][i]
        data_list = get_taxdata (company_name)
        df.loc[i,'企业名称':'银行账户'] = data_list

    df.to_csv('output1.csv',index=False)
except:
    df.to_csv('output1.csv',index=False)
