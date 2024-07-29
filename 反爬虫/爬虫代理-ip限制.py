# 拒绝服务 IP限制 封IP A->C 转化为 A->B->C
# http://www.ip3366.net
# https://www.kuaidaili.com/free/
import requests

# 白嫖的免费代理
proxies = {
    'http': 'http://27.70.38.29:6666',
    'https': 'https://27.70.38.29:6666',
}
try:
    response = requests.get('https://www.baidu.com', proxies = proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)


# 错误信息 需要抓取大量的免费代理 并且做可用性检测 构建一个代理IP池
# https://github.com/Python3WebSpider/ProxyPool