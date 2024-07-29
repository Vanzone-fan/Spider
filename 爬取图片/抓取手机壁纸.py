import requests
from bs4 import BeautifulSoup


class SpiderZol(object):
    """
    抓取手机壁纸 http://sj.zol.com.cn/bizhi/1080x1920/
    """

    def __init__(self, start_page=1, end_page=5):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        }
        # 手机壁纸网址
        self.target = "http://sj.zol.com.cn/bizhi/1080x1920"
        # 列表的地址列表
        self.page_urls = []
        self.image_urls = []
        # 需要抓取的列表页起始 及 结束
        self.start_page = start_page
        self.end_page = end_page

    def get_page_urls(self):
        """
        某一页的地址格式为
        http://sj.zol.com.cn/bizhi/1080x1920/N.html  N为具体那一页

        start_page: 开始的页数
        end_page: 结束的页数
        """

        self.page_urls = []
        for i in range(self.start_page, self.end_page + 1):
            self.page_urls.append("{}/{}.html".format(self.target, i))

        print("抓取的列表页如下:")
        print("\n".join(self.page_urls))

    def get_image_urls(self, page_url):
        """
        抓取列表页如
        http://sj.zol.com.cn/bizhi/1080x1920/1.html
        解析出其中所有的图集地址
         <a
            class="pic"
            href="/bizhi/detail_10981_121155.html"
            target="_blank"
            hidefocus="true"
            title = "中国最美公路227国道沿途风光"
        >
        """
        r = requests.get(page_url, headers=self.headers)
        bs = BeautifulSoup(r.text, "lxml")

        # 通过 <a class="pic"> 来定位解析
        for tag in bs.find_all("a", class_="pic"):
            image_name = tag.text.strip()  # 获取图集名
            image_url = tag.get("href", "")  # 获取href属性

            # 将数据放入对象变量image_urls 中
            print("解析出图集:《{}》 地址为:{}".format(image_name, image_url))
            self.image_urls.append({"image_name": image_name, "image_url": image_url})

    def go(self):
        self.get_page_urls()
        for page_url in self.page_urls:
            self.get_image_urls(page_url)


if __name__ == "__main__":
    spider = SpiderZol(1, 1)
    spider.go()