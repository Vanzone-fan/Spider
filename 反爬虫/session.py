import requests
# 请求参数+post / 手动获取+headers+get
class douban_login(object):
    def __init__(self,account,password):
        self.url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Referer":"https://accounts.douban.com/passport/login?redir=https%3A%2F%2Fbook.douban.com%2Ftag%2F%3Fview%3Dcloud"}
        self.data = {
        "ck":"" , "name": account , "password":password , "remember": "true" 
    }
        self.session = requests.Session()
        
    def get_cookie(self):
        html = self.session.post(url=self.url,headers=self.headers,data=self.data).json()
        if html["status"] == "success" :
            print("登录成功")
        else:
            print("登录失败")
            print(html)
            
    def get_user_order(self):
        url = "https://www.douban.com/mine/orders/"
        req = self.session.get(url,headers = self.headers)
        print(req.status_code)
        print(req.text)
        
    def run(self):
        self.get_cookie()
        self.get_user_order()
        
account = "your_account"
password = "your_password"
login = douban_login(account, password)
login.run()