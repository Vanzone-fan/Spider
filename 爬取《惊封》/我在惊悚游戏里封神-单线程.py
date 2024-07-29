# 我在惊悚游戏里封神 书的网址 https://m.junjh.com/xiaoshuo/39/39453/
# 具体某一章的内容 https://m.junjh.com/xiaoshuo/39/39453/19480534.html
import csv
from multiprocessing import Pool, cpu_count
import multiprocessing
import os
import time
from bs4 import BeautifulSoup

import requests
import sys
sys.setrecursionlimit(9000)

class SpiderNovel(object):
    def __init__(self):
        self.target = 'https://m.junjh.com/xiaoshuo/39/39453/'
        self.chapter_csv_dir = '《我在惊悚游戏里封神》'
        self.chapter_csv_file = os.path.join(self.chapter_csv_dir,'目录.csv')
        self.all_content_file = os.path.join(self.chapter_csv_dir,'全书内容.txt')
        self.init_save_dir()
        
    def init_save_dir(self):
        if not os.path.exists(self.chapter_csv_dir):
            try:
                os.mkdir(self.chapter_csv_dir)
            except Exception as e:
                pass
    
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
        
    # 对于每一个具体章节的链接 所有内容都存放在<div class="txt" id="txt"><p>内
    def check_lost(self,csv_datas):
        chapter_name = []
        chapter_url = []
        number_array = []

        for each in csv_datas:
            chapter_name.append(each['name'])
            chapter_url.append(each['url'])
        
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
                        
    def write_content(self,csv_datas):
        chapter_name = []
        chapter_url = []
        
        num = 0
        for each in csv_datas:
            chapter_name.append(each['name'])
            chapter_url.append(each['url'])
            
        chapter_title = [title + '.txt' for title in chapter_name]
        # 新建 txt
        for i in chapter_title:
            content_file = os.path.join(self.chapter_csv_dir,i)
            
            req = requests.get(url = chapter_url[num])
            novel = req.content.decode('utf-8')
            bs = BeautifulSoup(novel,'html.parser')
            p_tags = bs.find_all('p')
            content = str(p_tags[0]).replace("<br/>","\n")
            content = content.replace("<p>","")
            content = content.replace("</p>","")
            with open(content_file,'w',encoding='utf-8') as f:
                f.write(chapter_name[chapter_title.index(i)])
                f.write(content)
                f.write("============================================================")
            num += 1
            print("进程ID:{}".format(os.getpid()),i,"保存成功")

                
    def write_csv(self,fields,csv_datas):
        with open(self.chapter_csv_file,'w',newline='') as output_csv:
            output_writer = csv.DictWriter(output_csv,fieldnames = fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)
        
def spiderFun(csv_datas):
    spider = SpiderNovel()
    spider.write_content(csv_datas)

if __name__ == '__main__':
    st_time = time.time()
    spider_csv = SpiderNovel()
    csv_datas = spider_csv.spider_chapters()
    spider_csv.check_lost(csv_datas)
    
    # 单进程爬虫
    # spiderFun(csv_datas)
    
    # 把csv_datas分块
    # list_ele_list=[]
    # for i in range(0,len(csv_datas),10):
    #     module = csv_datas[i:i+10]
    #     list_ele_list.append(module)
        
    
    # with Pool(multiprocessing.cpu_count()) as p:
    #     p.map(spiderFun,list_ele_list)
    
    et_time=time.time()
    print("结束爬虫，耗时{}秒".format(et_time-st_time))
# spider.write_csv(['name','url'],csv_datas)
