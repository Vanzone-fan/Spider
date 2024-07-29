"""
一般爬虫的流程
发送请求 module : urllib.request || requests
解析网页 module : BeautifulSoup -- HTML & XML
定位标签
保存数据
"""
from bs4 import BeautifulSoup


html_content = """\
<!DOCTYPE html>
<html>
<head>
    <meta content="text/html;charset=utf-8" http-equiv="content-type" />
    <meta content="IE=Edge" http-equiv="X-UA-Compatible" />
    <meta content="always" name="referrer" />
    <link href="https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/bdorz/baidu.min.css" rel="stylesheet" type="text/css" />
    <title>百度一下，你就知道 </title>
</head>
<body link="#0000cc">
  <div id="wrapper">
    <div id="head">
        <div class="head_wrapper">
          <div id="u2">
            <a class="mnav" href="http://news.baidu.com" name="tj_trnews">新闻 </a>
            <a class="mnav" href="https://www.hao123.com" name="tj_trhao123">hao123 </a>
            <a class="mnav" href="http://map.baidu.com" name="tj_trmap">地图 </a>
            <a class="mnav" href="http://v.baidu.com" name="tj_trvideo">视频 </a>
            <a class="mnav" href="http://tieba.baidu.com" name="tj_trtieba">贴吧 </a>
            <a class="bri" href="//www.baidu.com/more/" name="tj_briicon" style="display: block;">更多产品 </a>
          </div>
        </div>
    </div>
  </div>
</body>
</html>
"""

bs = BeautifulSoup(html_content , "html.parser")   # 缩进格式
print(bs.prettify())   # 格式化html结构
print(bs.title) # 获取title标签的名称
print(bs.title.name) # 获取title的name
print(bs.title.string) # 获取title标签的所有内容
print(bs.head)
print(bs.div)  # 获取第一个div标签中的所有内容
print(bs.div["id"]) # 获取第一个div标签的id的值
print(bs.a)
print(bs.find_all("a")) # 获取所有的a标签
print(bs.find(id="u2")) # 获取id="u2"
for item in bs.find_all("a"):
    print(item.get("href")) # 获取所有的a标签，并遍历打印a标签中的href的值
for item in bs.find_all("a"):
    print(item.get_text())

