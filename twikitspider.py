import asyncio
from twikit import Client
import httpx
from datetime import datetime
import json
import os

USERNAME = 'sunny_jamerr'
EMAIL = '1765423653@qq.com'
PASSWORD = '1qaz@WSX12'

# USERNAME = 'frankyur169874'
# EMAIL = 'frankliuyujie@outlook.com'
# PASSWORD = '1qaz@WSX12'

# 设置代理
proxy = 'socks5://127.0.0.1:7897'


# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

# 初始化客户端
client = Client('en-US', proxy=proxy, timeout=30.0, headers=headers)

async def save_cookies():
    cookies = client.get_cookies()
    with open('/Users/cn/VScode/newspider/cookies.json', 'wb') as f:
        json.dump(cookies, f, ensure_ascii=True)

async def load_cookies():
    try:
        with open('/Users/cn/VScode/newspider/cookies.json', 'rb') as f:
            content = f.read()
            if not content:  # 如果文件为空
                return False
            cookies = json.loads(content.decode('utf-8'))
            await client.set_cookies(cookies)
            return True
    except (FileNotFoundError, json.JSONDecodeError):  # 处理文件不存在或JSON解析错误
        return False


async def main():
    # 尝试加载cookies
    if not await load_cookies():
        try:
            # 如果没有cookies，则登录
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
            # 保存cookies
            await save_cookies()
        except Exception as e:
            print(f"登录失败: {str(e)}")
            print("建议等待一段时间后再尝试登录")
            return  # 登录失败时退出程序
    
    try:
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取用户信息和推文
        user = await client.get_user_by_screen_name('elonmusk')
        tweets = await client.get_user_tweets(user.id, 'Tweets', count=3)  # 移除 exclude 参数
        
        # 写入文件
        with open('/Users/cn/VScode/newspider/context.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n采集时间：{current_time}\n")
            f.write("-" * 50 + "\n")
            
            for tweet in tweets:
                print('-' * 50)
                print(tweet.text)
                print('-' * 50)
                print()
                
                # 同时写入文件
                f.write(f"{tweet.text}\n\n")
                
            f.write("-" * 50 + "\n")
            f.write(f"结束时间：{current_time}\n")
    except Exception as e:
        print(f"获取或写入数据失败: {str(e)}")

asyncio.run(main())

