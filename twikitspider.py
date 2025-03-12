import asyncio
from twikit import Client
import httpx
from datetime import datetime, timezone, timedelta
import json
import os

# 设置常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'cookies.json')  # 新增cookies文件路径

# USERNAME = 'sunny_jamerr'
# EMAIL = '1765423653@qq.com'
# PASSWORD = '1qaz@WSX12'

# USERNAME = 'frankyur169874'
# EMAIL = 'frankliuyujie@outlook.com'
# PASSWORD = '1qaz@WSX12'

# USERNAME = 'salinna1735526'
# EMAIL = 'andersonlinqin@163.com'
# PASSWORD = '1qaz@WSX12'

USERNAME = 'EmilyGreen21447'
EMAIL = 'zhangyueqin0321@163.com'
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

# 修改常量定义
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ACCOUNT_LIST_FILE = os.path.join(DATA_DIR, 'accountlists.txt')
COOKIES_FILE = os.path.join(BASE_DIR, 'cookies.json')

# 添加新的常量定义
KEYWORDS_FILE = os.path.join(DATA_DIR, 'keywords.txt')
KEYWORDS_POSTS_FILE = os.path.join(DATA_DIR, 'keywordsposts.txt')

async def process_user(client, username):
    try:
        # 为每个用户创建对应的内容文件
        content_file = os.path.join(DATA_DIR, f'{username}_content.txt')
        
        user = await client.get_user_by_screen_name(username)
        tweets = await client.get_user_tweets(user.id, 'Tweets', count=3)
        
        # 读取已存在的推文ID
        existing_ids = set()
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("推文ID: "):
                        tweet_id = line.strip().split(": ")[1]
                        existing_ids.add(tweet_id)
        
        # 确保文件存在
        if not os.path.exists(content_file):
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(f"# Twitter 用户 {username} 数据采集记录\n\n")

        # 读取现有文件内容
        existing_content = ""
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = f"# Twitter 用户 {username} 数据采集记录\n\n"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_content = f"采集时间：{current_time}\n"
        new_content += "-" * 50 + "\n"
        
        has_new_tweets = False
        
        # 读取关键词列表
        keywords = []
        if os.path.exists(KEYWORDS_FILE):
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                keywords = [line.strip().lower() for line in f if line.strip()]
        
        # 设置北京时间时区 (UTC+8)
        beijing_tz = timezone(timedelta(hours=8))
        
        for tweet in tweets:
            if str(tweet.id) in existing_ids:
                print(f"用户 {username} 跳过重复推文 ID: {tweet.id}")
                continue
                
            has_new_tweets = True
            
            # 解析原始时间字符串并转换为北京时间
            # 示例格式: "Wed Mar 12 13:50:41 +0000 2025"
            utc_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S %z %Y")
            beijing_time = utc_time.astimezone(beijing_tz)
            
            tweet_info = (
                f"推文ID: {tweet.id}\n"
                f"发布时间: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"内容: {tweet.text}\n"
                f"点赞数: {tweet.favorite_count}\n"
                f"转发数: {tweet.retweet_count}\n"
                f"回复数: {tweet.reply_count}\n"
            )
            
            # 检查推文是否包含关键词
            tweet_text = tweet.text.lower()
            matched_keywords = [kw for kw in keywords if kw in tweet_text]
            
            if matched_keywords:
                print(f"用户 {username} 的推文匹配到关键词: {', '.join(matched_keywords)}")
                # 将匹配的推文保存到关键词推文文件
                with open(KEYWORDS_POSTS_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"\n{'='*50}\n")
                    f.write(f"用户: {username}\n")
                    f.write(f"匹配关键词: {', '.join(matched_keywords)}\n")
                    f.write(tweet_info)
                    f.write(f"{'='*50}\n")
            
            print(f"用户 {username} 新推文：")
            print('-' * 50)
            print(tweet_info)
            print('-' * 50)
            print()
            
            new_content += tweet_info + "\n"
            existing_ids.add(str(tweet.id))
        
        if not has_new_tweets:
            new_content += "无帖子更新！\n"
            
        new_content += "-" * 50 + "\n"
        new_content += f"结束时间：{current_time}\n\n"
        
        # 将新内容写入文件开头
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(new_content + existing_content)
            
    except Exception as e:
        print(f"处理用户 {username} 时出错: {str(e)}")

async def main():
    try:
        # 确保数据目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # cookies 处理部分
        cookies_loaded = False
        if os.path.exists(COOKIES_FILE):
            try:
                with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    client.set_cookies(cookies)
                    cookies_loaded = True
                    print("已从文件加载登录状态")
            except Exception as e:
                print(f"加载cookies失败: {e}")
                cookies = None
        
        # 如果没有cookies或加载失败，则重新登录
        if not cookies_loaded:
            try:
                await client.login(
                    auth_info_1=USERNAME,
                    auth_info_2=EMAIL,
                    password=PASSWORD
                )
                cookies = client.get_cookies()
                with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cookies, f)
                print("已保存登录状态")
            except UnicodeDecodeError:
                print("登录响应编码错误，正在重试...")
                await asyncio.sleep(2)
                await client.login(
                    auth_info_1=USERNAME,
                    auth_info_2=EMAIL,
                    password=PASSWORD
                )
                cookies = await client.get_cookies()
                with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cookies, f)
                print("已保存登录状态")
        
        # 读取用户列表
        if not os.path.exists(ACCOUNT_LIST_FILE):
            print("账号列表文件不存在！")
            return
            
        with open(ACCOUNT_LIST_FILE, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
        
        # 处理每个用户
        for username in usernames:
            print(f"\n开始处理用户: {username}")
            await process_user(client, username)
            await asyncio.sleep(1)  # 添加短暂延迟
            
    except Exception as e:
        error_msg = f"操作失败: {str(e).encode('ascii', 'ignore').decode('ascii')}"
        print(error_msg)
        try:
            with open(os.path.join(BASE_DIR, 'error.log'), 'a', encoding='utf-8', errors='ignore') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}\n")
        except Exception as write_error:
            print(f"写入错误日志失败: {str(write_error)}")

asyncio.run(main())