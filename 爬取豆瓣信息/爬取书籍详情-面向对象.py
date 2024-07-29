import csv
import re
import time

from bs4 import BeautifulSoup
import requests


class spider_douban_books(object):
    def __init__(self,book_list_csv_path,books_csv_path):
        # 需要抓取的书籍列表信息
        # 保存的书籍详细信息
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
        self.spider_book_infos = self.read_csv_file(book_list_csv_path)
        self.books_csv_path = books_csv_path
        self.all_book_infos = []
        
    def spider_one_book(self,book_info):
        req = self.try_request_url(book_info['book_url'])
        html_content = req.text
        ret = self.parse_book_info(book_info['book_id'],html_content)
        book_info.update(ret)
        self.all_book_infos.append(book_info)
    
    def parse_by_re(self,re_str,html_content):
        rets = re.findall(re_str,html_content)
        if len(rets)>0:
            return rets[0].strip()
        return ""
    
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
    
    def parse_book_info(self,book_id,html_content):
        bs = BeautifulSoup(html_content,"html.parser")
        
        price = self.parse_by_re('<span class="pl">定价:</span>(.*)<br/>',html_content)
        isbn = self.parse_by_re('<span class="pl">ISBN:</span>(.*)<br/>',html_content)
    
        content_summary_tag = bs.find('div', {'class': 'indent', 'id': 'link-report'})
        content_summary = content_summary_tag.text.strip()

        author_summary_tag = content_summary_tag.find_next('div', {'class': 'indent'})
        author_summary = author_summary_tag.text.strip() if author_summary_tag != None else ''
    
        catalog_tag = bs.find('div', {'class': 'indent', 'id': 'dir_%s_full' % book_id})
        catalog = catalog_tag.text.strip() if catalog_tag != None else ''
        
        if author_summary=="" or catalog=="":
            print(book_id)
            
        return {
            'price': price,
            'isbn': isbn,
            'content_summary': content_summary,
            'author_summary': author_summary,
            'catalog': catalog
        }
        
    def read_csv_file(self,csv_path):
        book_infos = []
        with open(csv_path, 'r' , encoding='utf-8') as pf:
            cool_csv_dict = csv.DictReader(pf)
            for row in cool_csv_dict:
                book_infos.append(row)
        return book_infos
    
    def save_to_csv(self):
        csv_datas = self.all_book_infos
        with open(self.books_csv_path, 'w', encoding='utf-8', newline='') as output_csv:
            fields = ["book_id","book_title","rate_score","rate_nums","book_pub_info","book_desc","book_url","pic_url","price","isbn","content_summary","author_summary","catalog"]
            output_writer = csv.DictWriter(output_csv,fieldnames = fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)
    
    def go(self):
        all_book_num = len(self.spider_book_infos)
        for i,book_info in enumerate(self.spider_book_infos):
            print(
                "进度:[{}/{}] 开始抓取书:{} {}".format(
                    i+1,all_book_num,book_info['book_title'],book_info['book_url']
                    ))
            self.spider_one_book(book_info)
            self.save_to_csv()
            print("结束抓取，书籍相关信息保存到了{}".format(self.books_csv_path))

st_time = time.time()            
spider = spider_douban_books("./爬取豆瓣信息/豆瓣书籍简介列表爬取结果.csv","./爬取豆瓣信息/豆瓣书籍详细信息爬取结果.csv")
spider.go()
et_time = time.time() 
print("耗时:%.2f秒"%(et_time-st_time))
