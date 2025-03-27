import json
import re

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


class Ablesci:
    name = ""
    isSign = False
    # 当前积分
    pointNow = 0
    # 连续签到天数
    signCount = 0

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd
        self.initSession()
        self.loadCookies()

    def login(self):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.ablesci.com",
            "priority": "u=1, i",
            "referer": "https://www.ablesci.com/site/login",
        }
        data = {
            "_csrf": self.getCsrfToken(),
            "email": self.email,
            "password": self.pwd,
            "remember": "on",
        }

        # 不返回数据 只修改cookies
        res = self.session.post(
            "https://www.ablesci.com/site/login",
            headers=headers,
            data=data,
        )
        print(res.text)
        self.checkLogin()
        self.saveCookies()

    def initSession(self):
        self.session = requests.Session()
        # 设置ua
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
            }
        )

    def loadCookies(self):
        """从文件加载cookies"""
        try:
            with open("cookies.json", "r") as f:
                all_cookies = json.load(f)
                if self.email in all_cookies:
                    self.session.cookies.update(all_cookies[self.email])
                    return True
                return False
        except FileNotFoundError:
            return False

    def saveCookies(self):
        """将cookies保存到文件"""
        try:
            with open("cookies.json", "r") as f:
                all_cookies = json.load(f)
        except FileNotFoundError:
            all_cookies = {}

        all_cookies[self.email] = dict(self.session.cookies)

        with open("cookies.json", "w") as f:
            json.dump(all_cookies, f)

    def getCsrfToken(self):
        """获取login页面html中的csrf"""
        response = self.session.get("https://www.ablesci.com/site/login")
        # 获取csrf
        # <meta name="csrf-token" content="7dsDmCOCc-81XVBeFo5EKlAPRfxkzU_MAv7iiV8u2H2j4zbVbs4HlQAfFSl_xS9hYGp1lSijO7hluIH-KBa8MA==">
        csrf = re.findall(r'<meta name="csrf-token" content="([^"]+)"', response.text)
        return csrf[0]

    def checkLogin(self):
        """检查是否登录 并获取用户名"""
        response = self.session.get("https://www.ablesci.com/")
        if "layui-nav able-head-user able-head-user-vip" in response.text:
            soup = BeautifulSoup(response.text, "html.parser")
            self.name = soup.find(
                "span", class_="mobile-hide able-head-user-vip-username"
            ).text
            self.pointNow = soup.find("cite", id="user-point-now").text
            self.signCount = soup.find("cite", id="sign-count").text
            return True
        return False

    def sign(self):
        """签到"""
        res = self.session.get("https://www.ablesci.com/user/sign").json()
        if res["code"] == 0:
            signPoint = res["data"]["signpoint"]
            print("签到奖励:", signPoint, "积分")
            return True
        elif "签到失败，您今天已于" in res["msg"]:
            print("重复签到")
        else:
            print(res["msg"])
        return False

    def printUserSingInfo(self):
        self.checkLogin()
        data = [["当前积分", self.pointNow], ["连续签到", f"{self.signCount}天"]]
        print(tabulate(data, tablefmt="simple_outline", colalign=("center", "center")))
