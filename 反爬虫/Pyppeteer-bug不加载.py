# 阅读JS代码
# 使用WebDriver无头浏览器 PhantomJS Selenium Pyppeteer
import requests
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
req = requests.get("https://edu.py2fun.com/learn#/course/list",headers=headers)

# <li class="_active_1nual_92">课程</li>
if req.text.find("课程")!=-1:
    print("含有课程信息")
else:
    print("不含有课程信息")

# print(req.text)
# 前后端分离

import asyncio
from pyppeteer import launch
async def get_url(fn,url):
    print("请求",url,"网页截图文件",fn)
    
    # 启动浏览器
    browser = await launch(headless = False)
    
    # 新建页面
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    
    # 转到url 关闭超时
    await page.goto(url,{'timeout':0})
    
    # 等待加载
    await page.waitFor(2000)
    content = await page.content()
    cookies = await page.cookies()
    
    if content.find("课程")!=-1:
        print("含有课程信息")
    else:
        print("不含有课程信息")
        
    # 输出截屏
    await page.screenshot({'path':fn})    
    
    await browser.close()
    
asyncio.get_event_loop().run_until_complete(get_url("./反爬虫/course_screenshot.png","https://edu.py2fun.com/learn#/course/list"))