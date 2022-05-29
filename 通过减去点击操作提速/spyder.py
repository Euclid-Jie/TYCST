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
    headers = {'cookie':'TYCID=082c0250c79111ecb0912bafcbc08352; ssuid=4261629120; creditGuide=1; RTYCID=b63f75e0df73490399169f0336fca903; _ga=GA1.2.887302821.1651218649; _gid=GA1.2.446782813.1651330828; jsid=https%3A%2F%2Fwww.tianyancha.com%2F%3Fjsid%3DSEM-BAIDU-PZ-SY-2021112-JRGW; bdHomeCount=0; searchSessionId=1651364924.10056270; aliyungf_tc=3d6fa519cf6eebacba637a0eb28f3de161ebcf0f25c350b07fd60ef76efc7ff0; acw_tc=76b20f5416513726521588735e5cda29b2a2da622b7ed8a76704ef5c2c2718; csrfToken=SHp6nmBLWsf7Z175Q05til_A; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22180744cb946746-0c97c6a024063a-12333272-921600-180744cb94787a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww2.bing.com%2F%22%7D%2C%22%24device_id%22%3A%22180744cb946746-0c97c6a024063a-12333272-921600-180744cb94787a%22%7D; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1651224161,1651330827,1651364925,1651372655; refresh_page=0; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1651373138; cloud_token=3b93748bb41b4a65a45aead5fd6b5f80',\
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
    
    url_head = 'https://www.tianyancha.com/cloud-wechat/qrcode.json?gid='
    response = requests.get(url_head+company_url.split('/')[-1]) #获取网页源码
    response.encoding = 'utf-8' #设置编码格式
    html = response.text #转换格式为html
    data_list = []
    for item in html.split(',')[4:10]:
        data_list.append(item.split(':')[1])
        
    return data_list



## 正式运行
path = getLocalFile() #获取文件路径
df = pd.read_excel(path) #读取文件为df
#添加空列
cols = ['企业名称','企业税号','企业地址','企业电话','开户银行','银行账户']
for item in cols:
    df[item] = np.nan


for i in range(0,100):
    company_name = df['公司名'][i]
    print(f"开始爬取{company_name}数据")
    data_list = get_taxdata (company_name)
    df.loc[i,'企业名称':'银行账户'] = data_list

df.to_csv('output1.csv',index=False)

