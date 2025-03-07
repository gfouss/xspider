import asyncio
from twikit import Client
import httpx

USERNAME = 'sunny_jamerr'
EMAIL = '1765423653@qq.com'
PASSWORD = '1qaz@WSX12'

# 设置代理
proxy = 'socks5://127.0.0.1:7897'


# 初始化客户端
client = Client('en-US', proxy=proxy,timeout=30.0)


async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    
    # 先获取用户信息
    user = await client.get_user_by_screen_name('elonmusk')
    # 使用用户 ID 获取推文
    tweets = await client.get_user_tweets(user.id, 'Tweets', count=1)
    for tweet in tweets:
        print(tweet.text)


asyncio.run(main())

