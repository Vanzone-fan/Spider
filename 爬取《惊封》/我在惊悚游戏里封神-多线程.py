# 将单线程的爬虫改为多线程爬虫
# 我在惊悚游戏里封神 书的网址 https://m.junjh.com/xiaoshuo/39/39453/
# 具体某一章的内容 https://m.junjh.com/xiaoshuo/39/39453/19480534.html
import csv
from multiprocessing import Pool, cpu_count
import multiprocessing
import os
import time
from bs4 import BeautifulSoup
import requests


class SpiderNovel(object):
    def __init__(self):
        self.target = 'https://m.junjh.com/xiaoshuo/39/39453/'
        self.chapter_csv_dir = '《我在惊悚游戏里封神》-多线程/'
        self.chapter_csv_file = os.path.join(self.chapter_csv_dir,'目录.csv')
        self.init_save_dir()
        
    def init_save_dir(self):
        if not os.path.exists(self.chapter_csv_dir):
            try:
                os.mkdir(self.chapter_csv_dir)
            except Exception as e:
                pass
    
    # 爬取小说目录上的章节标题和对应链接
    def spider_chapters(self):
        req = requests.get(url = self.target)
        html_content = req.content.decode('utf-8')
        bs = BeautifulSoup(html_content,'html.parser')
        ul_tags = []
        ul_tags.append(bs.find('ul',class_='chapter'))
        
        a_tags = ul_tags[0].find_all('a')
        
        csv_datas = []
        for each in a_tags:
            csv_datas.append({'name':each.string,'url':"https://m.junjh.com"+each['href']})
        return csv_datas
    
    # 保存小说章节标题和对应链接到csv文件里
    def write_csv(self,fields,csv_datas):
        with open(self.chapter_csv_file,'w',newline='') as output_csv:
            output_writer = csv.DictWriter(output_csv,fieldnames = fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)
                
    # 对于每一个具体章节的链接 所有内容都存放在<div class="txt" id="txt"><p>内
    def check_lost(self):
        tuple = self.seperate_csv_datas(self.spider_chapters())
        chapter_name = tuple[0]
        number_array = []
        
        for each in chapter_name:
            numbers =''.join(filter(str.isdigit,each))
            number = int(numbers[0:3])
            number_array.append(number)
        
        check = list(range(1,number_array[len(number_array)-1]+1))
        for i in check:
            if i not in number_array:
                if i!=52:
                    # 52章属于命名错误，文件仍然存在
                    with open(self.chapter_csv_dir + "/bug.txt",'a',encoding='utf-8') as f:
                        f.write("缺少第" + str(i) + "章信息" + '\n')
                    
    def seperate_csv_datas(self,csv_datas):
        chapter_name = []
        chapter_url = []

        for each in csv_datas:
            chapter_name.append(each['name'])
            chapter_url.append(each['url'])

        return chapter_name,chapter_url

    def new_file(self,chapter_name):
        chapter_title = [title + '.txt' for title in chapter_name]
        # 新建 txt
        for i in chapter_title:
            content_file = os.path.join(self.chapter_csv_dir,i)
            with open(content_file,'w',encoding='utf-8') as f:
                f.write(chapter_name[chapter_title.index(i)])
        return chapter_title    
        
    def write_content(self,url):
        csv_datas = self.spider_chapters()
        chapter_title = self.new_file(self.seperate_csv_datas(csv_datas)[0])
        req = requests.get(url)
        novel = req.content.decode('utf-8')
        bs = BeautifulSoup(novel,'html.parser')
        p_tags = bs.find_all('p')
        content = str(p_tags[0]).replace("<br/>","\n")
        content = content.replace("<p>","")
        content = content.replace("</p>","")
        for dict in csv_datas:
            if dict['url'] == url:
                index = csv_datas.index(dict)
        content_file = self.chapter_csv_dir + chapter_title[index]
        with open(content_file,'w',encoding='utf-8') as f:
            f.write(content)
            f.write("============================================================")
        print("进程ID:{}".format(os.getpid()),content_file,"保存成功")
                

        
def spiderFun(url):
    # 爬虫核心代码
    spider = SpiderNovel()
    spider.write_content(url)
        

if __name__ == '__main__':
    st_time = time.time()
    
    # 创建一个爬虫对象
    spider = SpiderNovel()
    
    # 获取[{}{}]
    csv_datas = spider.spider_chapters()
    
    # 先检验有没有不全的小说章节
    spider.check_lost()
    
    # 分离出小说章节的 标题 和 链接
    tuple = spider.seperate_csv_datas(csv_datas)
    chapter_name = tuple[0]
    
    # 根据小说章节名字新建各章节的txt文件
    chapter_title = spider.new_file(chapter_name)
    
    # url组成的列表 用于多进程参数传入
    chapter_url = tuple[1]
    
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(spiderFun,chapter_url)
    
    et_time=time.time()
    print("结束爬虫，耗时{}秒".format(et_time-st_time))
