import requests

#甚至不需要headers
headers = {'cookie':'TYCID=082c0250c79111ecb0912bafcbc08352; ssuid=4261629120; creditGuide=1; RTYCID=b63f75e0df73490399169f0336fca903; _ga=GA1.2.887302821.1651218649; _gid=GA1.2.446782813.1651330828; jsid=https%3A%2F%2Fwww.tianyancha.com%2F%3Fjsid%3DSEM-BAIDU-PZ-SY-2021112-JRGW; bdHomeCount=0; searchSessionId=1651364924.10056270; aliyungf_tc=3d6fa519cf6eebacba637a0eb28f3de161ebcf0f25c350b07fd60ef76efc7ff0; acw_tc=76b20f5416513726521588735e5cda29b2a2da622b7ed8a76704ef5c2c2718; csrfToken=SHp6nmBLWsf7Z175Q05til_A; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22180744cb946746-0c97c6a024063a-12333272-921600-180744cb94787a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww2.bing.com%2F%22%7D%2C%22%24device_id%22%3A%22180744cb946746-0c97c6a024063a-12333272-921600-180744cb94787a%22%7D; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1651224161,1651330827,1651364925,1651372655; refresh_page=0; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1651372687; cloud_token=e035d152c880425ba51a5f4f5e4edc38; cloud_utm=ffa6eb897ef440b1b5629dec24ae0417',\
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' }

url = 'https://www.tianyancha.com/cloud-wechat/qrcode.json?gid=673250640&_=1651372791752'
url2 = 'https://www.tianyancha.com/cloud-wechat/qrcode.json?gid=817637971&_=1651373135585'
url3 = 'https://www.tianyancha.com/cloud-wechat/qrcode.json?gid=817637971'
response = requests.get(url3,headers=headers) #获取网页源码

response.encoding = 'utf-8' #设置编码格式
html = response.text #转换格式为html
print(html)