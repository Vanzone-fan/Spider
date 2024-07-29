"""
小说站点 https://www.biqukan.cc/
《凡人修仙之仙界篇》https://www.biqukan.cc/article/30067/

最后生成一个txt文件包含小说全文
但更推荐每一章单独保存txt文件

且单线程下载速度太慢，每秒几乎只能完成万分之二左右下载任务

依赖编辑器，后期可以做成可视化窗口打包成可执行文件

"""
import csv
import os.path

import requests

from bs4 import  BeautifulSoup
class SpiderBiqukan(object):
    def __init__(self,article_id:int):
        #param: article_id 30067 改变传入的参数就可以改变爬取的书目
        self.target = f'https://www.biqukan.cc/article/{article_id}/'
        self.chapter_csv_dir = f'novel-{article_id}'

        self.chapter_csv_file = os.path.join(self.chapter_csv_dir,'目录.csv')
        self.all_content_file = os.path.join(self.chapter_csv_dir,'小说内容.txt')

        self.init_save_dir()
    def init_save_dir(self):
        if not os.path.exists(self.chapter_csv_dir):
            try:
                os.mkdir(self.chapter_csv_dir)
            except Exception as e:
                pass
    def spider_chapters(self):
        req = requests.get(url=self.target)
        html_content = req.content.decode('gbk')
        bs = BeautifulSoup(html_content,"html.parser")
        ul_tags = bs.find_all('ul',class_='mulu_list')
        a_tags = ul_tags[0].find_all('a')
        csv_datas = []
        for each in a_tags:
            csv_datas.append({'name':each.string,'url':self.target+each.get('href')})
        return csv_datas
    def write_content(self,text):
        write_flag = True
        with open(self.all_content_file,'a',encoding='utf-8') as f:
            f.write(text)
            f.write('==========================================')
    def spider_content(self,contentname,contenthref):
        cnt = 0
        for each in contenthref:
            req = requests.get(url=each)
            try:
                html = req.content.decode('gbk')
            except Exception as e:
                html = req.text
            bf = BeautifulSoup(html,'html.parser')
            text_tag = bf.find('div',id='htmlContent',class_='chapter-content')
            title = contentname[cnt]
            content = text_tag.text.replace(" ","\n")
            text = title + content

            self.write_content(text)
            cnt +=1
            print('已下载:%.3f%%' % float(cnt / len(contenthref)))
    def write_csv(self,fields,csv_datas):
        with open(self.chapter_csv_file,'w',newline = '') as output_csv:
            output_writer = csv.DictWriter(output_csv,fieldnames = fields)
            output_writer.writeheader()
            for item in csv_datas:
                output_writer.writerow(item)


spider = SpiderBiqukan(30067)
print('开始抓取章节信息')
csv_datas = spider.spider_chapters()
contenthref=[]
contentname=[]
for i in csv_datas:
    contentname.append(i['name'])
    contenthref.append(i['url'])
print('保存章节信息到：%s' % (spider.chapter_csv_file))
spider.write_csv(['name','url'],csv_datas)
for i in contentname:
    print(i)

print('开始抓取具体章节内容:')
spider.spider_content(contentname,contenthref)


print('下载完成')