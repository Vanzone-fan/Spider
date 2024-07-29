'''
爬取
    审查 请求 解析 保存 加速
反爬
    身份识别 爬虫行为 数据加密
身份识别
    UA/referer/cookie 添加字段 使用UA池 模拟登录
请求参数
    html静态获取 发送请求 js生成-js2py获取/selenium 验证码-打码平台/机器学习
爬虫行为
    购买ip 请求之间随机等待-代理池/随机休眠账号 控制请求频率和次数
数据加密
    自定义-切换手机版/解析字体文件 css-计算偏移 js生成 编码格式
'''
'''模拟登录
POST请求 获取登录的URL并填写请求体参数 然后 POST 请求登录 相对麻烦
添加Cookies 先登录将获取到的 Cookies 加入 Headers 中 方便
'''
import requests
def login_douban(account,password):
    url = "https://accounts.douban.com/j/mobile/login/basic"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Referer":"https://accounts.douban.com/passport/login?redir=https%3A%2F%2Fbook.douban.com%2Ftag%2F%3Fview%3Dcloud"}
    data = {
        "ck":"" , "name": account , "password":password , "remember": "true" 
    }
    req = requests.post(url,headers=headers,data=data)
    print(req.text)
    
login_douban(123456,456789)