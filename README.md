

# 科研通自动签到

自动签到 可部署青龙面板

 
## 快速开始
支持设置多个账户

### 1. 配置账户信息

新建一个`users.json`文件 内容格式如下
``` json
{
  "your email 1": "password",
  "your email 2": "password"
 }
```
### 2. 运行main.py
本地运行
```
python main.py
```
或者青龙面板设置定时任务
```
task 项目路径/main.py
```

