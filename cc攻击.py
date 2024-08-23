
import requests
from concurrent.futures import ThreadPoolExecutor
import random

# 动态请求参数
def get_dynamic_params():
    return {
        'query': ''.join(random.choice(string.ascii_letters) for _ in range(10)),
        'page': random.randint(1, 100)
    }

def send_request(url, params):
    try:
        response = requests.get(url, params=params)
        print(response.status_code)
    except requests.exceptions.RequestException as e:
        print(str(e))

if __name__ == "__main__":
    urls = ['https://example.com']  # 替换为目标URL
    num_requests = 100  # 要发送的请求数量
    threads = 10  # 并行线程的数量

    # 动态用户代理
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12)',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5X Build/MMB29M)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)'
    ]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(send_request, url, params): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            params = get_dynamic_params()
            try:
                data = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (url, exc))
