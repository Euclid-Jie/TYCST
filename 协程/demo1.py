# python 源码
import asyncio
import requests
import time


async def result(url):
    res = await request_url(url)
    print(res)


async def request_url(url):
    res = requests.get(url)
    await asyncio.sleep(1)
    print("execute_time:", time.time() - start)
    return res


url_list = ["https://www.csdn.net/",
            "https://blog.csdn.net/qq_43380180/article/details/111573642",
            "https://www.baidu.com/",
            ]

start = time.time()
print(f"start_time:{start}\n")

task = [result(url) for url in url_list]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))

endtime = time.time() - start
print("\nendtime:", time.time())
print("all_execute_time:", endtime)
