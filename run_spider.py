import subprocess
import time
import random
from datetime import datetime

def run_spider():
    try:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行爬虫...")
        subprocess.run(['python3', './twikitspider.py'])
    except Exception as e:
        print(f"执行出错: {str(e)}")

def main():
    while True:
        run_spider()
        # 随机等待3-10分钟
        wait_time = random.randint(180, 600)
        print(f"\n等待 {wait_time} 秒后继续...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()