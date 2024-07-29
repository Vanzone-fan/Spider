import csv

import requests
from bs4 import BeautifulSoup
mulu_target = 'https://www.biqukan.cc/article/30067/'
mulu_req = requests.get(url=mulu_target)


# print(req.text)

# bs = BeautifulSoup(req.text,"html.parser")
# bs_pre = bs.prettify()
# print(bs_pre)

# print(req.apparent_encoding)    
# print(req.encoding)             

# <a href="https://www.biqukan.cc/article/14650/" target="_blank" title="??????V?">

req_decode = mulu_req.content.decode('gbk') #req.encoding = 'gbk'
bs_decode = BeautifulSoup(req_decode,"html.parser")
bs_decode_pre = bs_decode.prettify()
# print(bs_decode_pre)

with open('??????????c????g?[???.txt', 'w',encoding='utf-8') as file:
    file.write(bs_decode_pre)

ul_tags = bs_decode.find_all('ul',class_='mulu_list')
a_tags = ul_tags[0].find_all('a')
csv_datas = []
for each in a_tags:
    # print(each.string,target + each.get('href'))
    csv_datas.append({'name':each.string,'url': mulu_target + each.get('href')})


with open('章节名称及超链接.csv','w',newline='') as output_csv:
    fields = ['name','url']
    output_writer = csv.DictWriter(output_csv,fieldnames=fields)
    output_writer.writeheader()
    for item in csv_datas:
        output_writer.writerow(item)

content_target = mulu_target + '17748491.html'
content_req = requests.get(url=content_target)
bf=BeautifulSoup(content_req.content.decode('gbk'),'html.parser')
source = bf.prettify()
with open('第一章-狐女-source.txt','w',encoding='utf-8') as f:
    f.write(source)

text_tags = bf.find('div',id='htmlContent',class_='chapter-content')
# print(text_tags.text)
content1 = text_tags.text.replace(" ","\n")
print(content1)
with open ('第一章-狐女.txt','w',encoding='utf-8') as contentfile:
    contentfile.write(content1)