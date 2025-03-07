import asyncio
from twikit import Client
import httpx

USERNAME = 'sunny_jamerr'
EMAIL = '1765423653@qq.com'
PASSWORD = '1qaz@WSX12'

# 初始化客户端
client = Client('en-US')

async def main():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    #await client.create_tweet(text='Why can not a nose be 12 inches long? Because then it would be a foot.')
    
    tweets = await client.get_user_tweets('elonmusk', 'Tweets',count=1)
    for tweet in tweets:
        print(tweet.text)

asyncio.run(main())

