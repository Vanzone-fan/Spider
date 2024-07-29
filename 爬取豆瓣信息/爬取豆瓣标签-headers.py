# 爬取 书籍类型 数量 地址
from bs4 import BeautifulSoup
import requests


def spider_tag():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}    
    req = requests.get(url = "https://book.douban.com/tag/?view=cloud",headers = headers)
    html_content = req.content.decode('utf-8')

    bs4 = BeautifulSoup(html_content, 'html.parser')

    table_tags = bs4.find('table',class_='tagCol')
    print(table_tags)
    a_tags = table_tags.find_all('a')
    for a_tag in a_tags:
        # <a href="/tag/小说">小说</a><b>(7515099)</b>
        
        print(a_tag.text.strip())
        
        print(a_tag.get('href',''))
        
        print(a_tag.find_next('b').text.strip()[1:-1])
spider_tag()