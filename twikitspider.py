import asyncio
from twikit import Client

USERNAME = 'sunny_jamerr'
EMAIL = '1765423653@qq.com'
PASSWORD = '1qaz@WSX12'

# 初始化客户端
client = Client('en-US')

async def main():
    await client.login(
        auth_info_1=USERNAME ,
        auth_info_2=EMAIL,
        password=PASSWORD
    )

asyncio.run(main())