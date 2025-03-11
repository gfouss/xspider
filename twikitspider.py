import asyncio
from twikit import Client
import httpx
from datetime import datetime
import json
import os

# 设置常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(BASE_DIR, 'context.txt')

# USERNAME = 'sunny_jamerr'
# EMAIL = '1765423653@qq.com'
# PASSWORD = '1qaz@WSX12'

# USERNAME = 'frankyur169874'
# EMAIL = 'frankliuyujie@outlook.com'
# PASSWORD = '1qaz@WSX12'

USERNAME = 'salinna1735526'
EMAIL = 'andersonlinqin@163.com'
PASSWORD = '1qaz@WSX12'

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
client = Client('en-US', proxy=proxy, timeout=30.0)

# 删除 get_tweets_with_retry 函数

async def main():
    try:
        # 直接登录
        try:
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
        except UnicodeDecodeError:
            print("登录响应编码错误，正在重试...")
            # 使用二进制模式处理响应
            await asyncio.sleep(2)  # 等待2秒后重试
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 获取用户信息和推文，直接获取不重试
        user = await client.get_user_by_screen_name('elonmusk')
        tweets = await client.get_user_tweets(user.id, 'Tweets', count=3)
        
        # 读取已存在的推文ID
        existing_ids = set()
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("推文ID: "):
                        tweet_id = line.strip().split(": ")[1]
                        existing_ids.add(tweet_id)
        
        # 确保文件存在
        if not os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
                f.write("# Twitter 数据采集记录\n\n")

        # 写入文件
        with open(CONTEXT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n采集时间：{current_time}\n")
            f.write("-" * 50 + "\n")
            
            has_new_tweets = False  # 添加标记
            
            for tweet in tweets:
                # 检查推文ID是否已存在
                if str(tweet.id) in existing_ids:
                    print(f"跳过重复推文 ID: {tweet.id}")
                    continue
                    
                has_new_tweets = True  # 有新推文时设置标记
                tweet_info = (
                    f"推文ID: {tweet.id}\n"
                    f"发布时间: {tweet.created_at}\n"
                    f"内容: {tweet.text}\n"
                    f"点赞数: {tweet.favorite_count}\n"
                    f"转发数: {tweet.retweet_count}\n"
                    f"回复数: {tweet.reply_count}\n"
                )
                
                print('-' * 50)
                print(tweet_info)
                print('-' * 50)
                print()
                
                f.write(tweet_info + "\n")
                existing_ids.add(str(tweet.id))  # 添加到已存在ID集合
            
            if not has_new_tweets:
                f.write("无帖子更新！\n")
                
            f.write("-" * 50 + "\n")
            f.write(f"结束时间：{current_time}\n")
            
    except Exception as e:
        error_msg = f"操作失败: {str(e).encode('ascii', 'ignore').decode('ascii')}"
        print(error_msg)
        try:
            with open(os.path.join(BASE_DIR, 'error.log'), 'a', encoding='utf-8', errors='ignore') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}\n")
        except Exception as write_error:
            print(f"写入错误日志失败: {str(write_error)}")

asyncio.run(main())