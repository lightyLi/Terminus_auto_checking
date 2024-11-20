# [Terminus 终点站](https://t.me/EmbyPublic) Emby 自动签到脚本

由 [emby-server-checkin](https://github.com/gqbre/emby-server-checkin) 提供思路


> 使用Google的Germini 来识别图片并返回结果，自动点击对应的选项
> 使用telethon库对telegram进行操作。

## 特点
+ 使用Germini来识别图片，识别准确率高，且 **gemini-1.5-flash** 模型可以免费使用
+ 支持多账号签到
+ 支持日志记录
+ 支持添加代理（还在路上）
+ 支持Docker自动配置（还在测试中）

## 1) 安装环境
1. 下载代码
```shell
git clone
```
2. 安装对应的包
```shell
cd 
touch .env
pip3 install -r requirements.txt
```

## 2) Telegram 账号登录
首先前往[Telegram 官网](https://my.telegram.org)申请 Application API。登陆后选择 API development tools，自行填写信息后提交后即可获取 api_id 和 api_hash。

> 注意：api_id和api_hash非常重要，有这两个信息可以直接控制账号，千万记得保护好。我把.env和session文件都加入.gitignore中，确保了不会传到github上。你也可以把这两个变量设为系统变量。

**.env**文件存储Germini的api key，以及多个账户的api_id和api_hash。在其中填上对应数据。
如图所示:
![.env文件示例](Screenshot%202024-11-21%20at%2002.54.17.png)
## 3) Google germini api获取
查看博客 [Gemini Pro 免费 API key 获取方法](https://hoyo.win/llm/get-gemini/)

## 4) 运行代码
在命令行中：
```shell
python3 terminus.py
```
第一次运行的时候需要登录，根据提示在命令行中输入tg注册的电话和验证码。如果有多个账号的话，每个账号都需要输入。
第一次登录过后，会自动生成session文件，后面即可自动登录。


## 5) 定时执行

将程序加入 cron 定时执行
```shell
crontab -e
```

在最后一行输入

```shell
0 2 * * * cd /root/emby-server-checkin && python3 terminus.py 2>&1
```

替换为你的项目路径，保存退出后自动签到程序将在 UTC+8 的 10:00, 10:05 分自动签到
