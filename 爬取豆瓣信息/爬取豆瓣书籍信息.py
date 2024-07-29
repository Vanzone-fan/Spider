import csv
import json
import time
from bs4 import BeautifulSoup, Tag
import requests

class spider_douban_list(object):
    def __init__(self,tag_name,start_page,end_page,csv_file_path):
        self.page_url_fomart = "https://book.douban.com/tag/%s?start={}&type=T" % (tag_name)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
        self.start_page = start_page
        self.end_page = end_page
        self.all_book_infos = []
        self.book_info_csv_path = csv_file_path
        
    def spider_one_page(self,page_num):
        print("开始抓取第{}页数据".format(page_num))
        page_url = self.page_url_fomart.format((page_num)-1)*20
        req = self.try_request_url(page_url)
        html_content = req.content.decode("utf-8")
        book_infos = self.parse_books_info(html_content)
        print("结束抓取第{}页数据，正确解析出{}本书".format(page_num,len(book_infos)))
        self.all_book_infos.extend(book_infos)
    
    def parse_books_info(self,html_content):
        bs = BeautifulSoup(html_content,"html.parser")
        sub_item_tags = bs.find_all('li',class_='subject-item')
        book_infos = []
        for sub_item_tag in sub_item_tags:
            if not isinstance(sub_item_tag,Tag):
                continue
            cur_book_title = ''
            try:
                pic_url = sub_item_tag.find('div',class_='pic').find('a').find('img')['src']
                div_book_info_tag = sub_item_tag.find('div',class_='info')
                book_url = div_book_info_tag.find('h2').find('a')['href']
                book_title = div_book_info_tag.find('h2').find('a')['title']
                cur_book_title = book_title
                book_pub_info = div_book_info_tag.find('div',class_='pub').text.strip()
                rate_score = div_book_info_tag.find('div',class_='star clearfix').find('span',class_='rating_nums').text.strip()
                rate_nums = div_book_info_tag.find('div',class_='star clearfix').find('span',class_='pl').text.strip()
                book_desc = div_book_info_tag.find('p').text.strip()
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
                book_infos.append(book_info)
            except Exception as e:
                print('error for',cur_book_title)
                print(e)
        return book_infos
    
    def try_request_url(self,url):
        try_num = 3
        i = 0
        req = None
        while i < try_num:
            req = requests.get(url, headers=self.headers)
            if req.status_code == 200:
                return req
            print(req.status_code,'尝试重新抓取',url)
            print(req.text)
            time.sleep(2)
            i+=1
        return req
    # print(json.dumps(books_infos,ensure_ascii=False,indent=2))
    def save_to_csv(self):
        """
        保存到本地的csv文件中
        """

        csv_datas = self.all_book_infos
        with open(self.book_info_csv_path, "w",encoding="utf-8") as output_csv:
            fields = [
                "book_id",
                "book_title",
                "rate_score",
                "rate_nums",
                "book_pub_info",
                "book_desc",
                "book_url",
                "pic_url",
            ]
            output_writer = csv.DictWriter(output_csv, fieldnames=fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)

    def go(self):
        # 循环抓取每页数据 并且解析书籍信息
        for page in range(self.start_page, self.end_page + 1):
            self.spider_one_page(page)

        # 保存数据到csv
        self.save_to_csv()


if __name__ == "__main__":
    # 示例代码仅抓取前5页的数据
    spider = spider_douban_list("编程", 1, 5, "./爬取豆瓣信息/豆瓣书籍简介列表爬取结果.csv")
    spider.go()
