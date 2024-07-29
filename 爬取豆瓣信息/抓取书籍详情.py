import re
import requests
from bs4 import BeautifulSoup
from bs4 import Tag

def parse_by_re(re_str,html_content):
    rets = re.findall(re_str,html_content)
    if len(rets)>0:
        return rets[0].strip()
    return ""

    """
    book_info = {
                    'pic_url': pic_url,
                    'book_url': book_url,
                    'book_title': book_title,
                    'book_pub_info': book_pub_info,
                    'rate_score': rate_score,
                    'rate_nums': rate_nums,
                    'book_desc': book_desc,
                    'book_id': book_url.split("subject/")[-1].replace("/", ''),
                }
    """

def spider_one_book(book_info):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'} 
    html_content = requests.get(book_info['book_url'],headers=headers).text
    bs = BeautifulSoup(html_content,'html.parser')
    
    price = parse_by_re('<span class="pl">定价:</span>(.*)<br/>',html_content)
    isbn = parse_by_re('<span class="pl">ISBN:</span>(.*)<br/>',html_content)
    
    content_summary_tag = bs.find('div', {'class': 'indent', 'id': 'link-report'})
    content_summary = content_summary_tag.text.strip()

    author_summary_tag = content_summary_tag.find_next('div', {'class': 'indent'})
    author_summary = author_summary_tag.text.strip() if author_summary_tag != None else ''
    
    catalog_tag = bs.find('div', {'class': 'indent', 'id': 'dir_%s_full' % book_info['book_id']})
    catalog = catalog_tag.text.strip() if catalog_tag != None else ''

    print(price)
    print(isbn)
    print(content_summary)
    print(author_summary)
    print(catalog)


spider_one_book({
    "book_id": "26829016",
    "book_title": "Python编程",
    "rate_score": "9.1",
    "rate_nums": "(3311人评价)",
    "book_pub_info": "[美] 埃里克·马瑟斯 / 袁国忠 / 人民邮电出版社 / 2016-7-1 / 89.00元",
    "book_desc": "本书是一本针对所有层次的Python 读者而作的Python 入门书。全书分两部分：第一部分介绍用Python 编程所必须了解的基本概念，包括matplot...",
    "book_url": "https://book.douban.com/subject/26829016/",
    "pic_url": "https://img9.doubanio.com/view/subject/s/public/s28891775.jpg"
})
    