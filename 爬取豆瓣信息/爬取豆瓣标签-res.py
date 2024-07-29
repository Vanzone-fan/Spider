from bs4 import BeautifulSoup,Tag
import requests
import re
def spider_tag_by_re():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'} 
    html_content =  requests.get('https://book.douban.com/tag/?view=cloud', headers=headers).text
    # <a href="/tag/小说">小说</a><b>(6694973)</b>
    rets = re.findall('<a href="(.*)">(.*)</a><b>(.*)</b>',html_content)
    # print(rets)
    for item in rets:
        print(item)
    

spider_tag_by_re()