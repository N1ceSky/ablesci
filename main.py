import json
import time

from ablesci import Ablesci

with open("users.json", "r") as f:
    users = json.load(f)
for email, pwd in users.items():
    print("=" * 20)
    print(email, "开始签到")
    ablesci = Ablesci(email, pwd)
    if not ablesci.checkLogin():
        ablesci.login()
    print(ablesci.name, "登录成功")
    ablesci.printUserSingInfo()
    time.sleep(3)
    if ablesci.sign():
        time.sleep(3)
        ablesci.printUserSingInfo()
    # 如果还有未处理的账号 则等待10秒
    if email != list(users.keys())[-1]:
        time.sleep(10)
