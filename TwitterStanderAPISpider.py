import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

proxies = {
    'http': 'http://your_proxy_address:your_proxy_port',
    'https': 'http://your_proxy_address:your_proxy_port'
}

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 accountlists.txt 文件的路径
accounts_file_path = os.path.join(current_dir, 'data', 'accountlists.txt')

# 构建 content.txt 文件的路径
content_file_path = os.path.join(current_dir, 'data', 'content.txt')

try:
    # 读取 accountlists.txt 文件中的 URL 列表
    with open(accounts_file_path, 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()

    # 打开 content.txt 文件以写入爬取的内容
    with open(content_file_path, 'w', encoding='utf-8') as output_file:
        for url in urls:
            try:
                # 发送 HTTP 请求获取网页内容
                response = requests.get(url,headers=headers)
                response.raise_for_status()  # 检查请求是否成功

                # 获取网页内容
                content = response.text

                # 打印网页内容
                print(f"URL: {url}")
                print(content)
                time.sleep(5)  # 每次请求后等待 5 秒

                # 将 URL 和对应的网页内容写入 content.txt 文件
                output_file.write(f"URL: {url}\n")
                output_file.write(content + '\n\n')

            except requests.RequestException as e:
                print(f"请求 {url} 时出错: {e}")
            except Exception as e:
                print(f"处理 {url} 时出现未知错误: {e}")

except FileNotFoundError:
    print(f"未找到 {accounts_file_path} 文件，请检查文件路径和文件名。")
except Exception as e:
    print(f"发生未知错误: {e}")