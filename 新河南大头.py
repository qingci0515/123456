import requests
import base64
import json
import ddddocr
import os
from PIL import Image
Image.ANTIALIAS = Image.LANCZOS
orc = ddddocr.DdddOcr()

path = os.path.dirname(os.path.realpath(__file__))

name = input("姓名")
sfz = input("身份证")
qq = "http://222.143.34.122:8092/code"

response = requests.get("http://222.143.34.122:8092")
cookies = response.cookies

head = {
    "Cookie": "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies]),
}

res = requests.get(qq,headers=head).text
resj = json.loads(res)
data = resj['data']
with open('hnyzm.jpg', 'wb') as file:
    data = base64.b64decode(data)
    yzm = data
yzm = orc.classification(yzm)
print(yzm)
print(yzm)

url = "http://222.143.34.122:8092/login"

data = {"personId":sfz,"personName":name,"code":yzm}

head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8",
    "Content-Length": "73",
    "Content-Type": "application/json",
    "Cookie": "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies]),
    "Host": "222.143.34.122:8092",
    "Origin": "http://222.143.34.122:8092",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://222.143.34.122:8092/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

dtres = requests.post(url,data=json.dumps(data),headers=head).text
dtresj = json.loads(dtres)
pd = dtresj['code']
if pd == "300":
    print("验证码获取异常！请重新请求")
else:
    if pd != "200":
        print("查询失败")
    else:
        data = dtresj['data']
        dt = data['faceStr']
        with open(f"{path}/hndt.jpg", "wb") as f:
            f.write(base64.b64decode(dt))
            hndt = open(f'{path}/hndt.jpg', 'rb')
            hndt.close()
