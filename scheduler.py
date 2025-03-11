import subprocess
import time
import random
from datetime import datetime
import os

def run_spider():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        spider_script = os.path.join(current_dir, 'twikitspider.py')
        
        # 运行爬虫脚本
        subprocess.run(['python3', spider_script], check=True)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 爬虫运行完成")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 爬虫运行失败: {e}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 发生错误: {e}")

def main():
    print("定时爬虫启动...")
    
    while True:
        # 运行爬虫
        run_spider()
        
        # 生成3-12分钟的随机等待时间（以秒为单位）
        wait_time = random.randint(3 * 60, 12 * 60)
        next_run = datetime.now().timestamp() + wait_time
        print(f"下次运行时间: {datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 等待指定时间
        time.sleep(wait_time)

if __name__ == "__main__":
    main()