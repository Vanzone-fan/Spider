import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}
r = requests.get("http://sj.zol.com.cn/bizhi/detail_10981_121155.html", headers=headers)
bs = BeautifulSoup(r.text, "lxml")

# 通过 <img id="bigImg"> 来定位解析出图片的真实地址
"""
image 标签
<img
    id="bigImg"
    src="https://sjbz-fd.zol-img.com.cn/t_s320x510c5/g6/M00/0E/07/ChMkKV-NICeIOAUKAEr-VrVkwWAAAD5UQDbYv8ASv5u449.jpg"
    width="320"
    height="510"
    alt=""
/>
"""
for tag in bs.find_all("img", id="bigImg"):
    # 解析出图片地址，并请求下载保存数据
    print(tag.get("src"))