import csv
import re
import time

import requests


class spider_douban_tag(object):
    def __init__(self,csv_file_path):
        self.target = 'https://book.douban.com/tag/?view=cloud'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'} 
        self.all_tag_infos = []
        self.tag_csv_path = csv_file_path
        
    def spider_tag(self):
        req = self.try_request_url(self.target)
        html_content = req.content.decode('utf-8')
        
        rets = re.findall('<a href="(.*)">(.*)</a><b>(.*)</b>', html_content)
        for item in rets:
            tmp = {
                'href':item[0].strip(),
                'name':item[1].strip(),
                'num':item[2].strip()
            }
            self.all_tag_infos.append(tmp)
            
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
    
    def save_to_csv(self):
        csv_datas = self.all_tag_infos
        with open(self.tag_csv_path, 'w', newline='', encoding='utf-8') as f:
            fields=['name','num','href']
            output_writer = csv.DictWriter(f,fieldnames=fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)
    
    def run(self):
        print("开始抓取")
        self.spider_tag()
        print("共抓取到书籍标签%s个" % len(self.all_tag_infos))
        self.save_to_csv()
        print("抓取完成，结果保存在%s" % self.tag_csv_path)

spider = spider_douban_tag('./爬取豆瓣信息/豆瓣书籍标签抓取结果表.csv')
spider.run()            