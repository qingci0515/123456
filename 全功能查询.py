import requests
import base64
import urllib3
import sys
import os
import subprocess

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request_with_retries(url, params=None, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= max_retries:
                return {"error": str(e)}

def check_phone_location():
    while True:
        phone_number = input("请输入要查询的手机号(输入exit退出): ")
        if phone_number.lower() == 'exit':
            break
        url = f"https://api.songzixian.com/api/phone-location?dataSource=PHONE_NUMBER_LOCATION&phoneNumber={phone_number}"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{phone_number}: 请求失败，错误信息: {result['error']}")
        else:
            if result['code'] == 200:
                data = result['data']
                print(f"手机号: {data['phoneNumber']}\n省份: {data['province']}\n城市: {data['city']}\n运营商: {data['carrier']}\n邮政编码: {data['postalCode']}")
            else:
                print(f"{phone_number}: 查询失败，返回信息: {result['message']}")
        print()

def check_ip_location():
    while True:
        mode = input("请选择查询模式(0: 国内定位, 1: 全球定位, 输入exit退出): ")
        if mode.lower() == 'exit':
            break
        ip = input("请输入要查询的IP地址(输入exit退出): ")
        if ip.lower() == 'exit':
            break
        if mode == '0':
            url = f"https://tools.mgtv100.com/external/v1/amap/ip?ip={ip}"
        else:
            url = f"https://app.ipdatacloud.com/v2/free_query?ip={ip}"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{ip}: 请求失败，错误信息: {result['error']}")
        else:
            if mode == '0' and result['status'] == 'success':
                data = result['data']
                print(f"IP地址: {ip}\n省份: {data['province']}\n城市: {data['city']}\n邮政编码: {data['adcode']}\n经纬度: {data['rectangle']}")
            elif mode == '1' and result['code'] == 200:
                data = result['data']
                print(f"IP地址: {ip}\n国家: {data['country']}\n省份: {data['province']}\n城市: {data['city']}\nISP: {data['isp']}")
            else:
                print(f"{ip}: 查询失败，返回信息: {result.get('info', result.get('msg'))}")
        print()

def check_address_coordinates():
    while True:
        address = input("请输入要查询的地址(输入exit退出): ")
        if address.lower() == 'exit':
            break
        params = {'id': '10000798', 'key': '519cbc79701652ca45f89eec512133ae', 'address': address}
        url = "https://cn.apihz.cn/api/other/jwbaidu.php"
        result = request_with_retries(url, params=params)
        if 'error' in result:
            print(f"{address}: 请求失败，错误信息: {result['error']}")
        else:
            if result['code'] == 200:
                print(f"地址: {address}\n经度: {result['lng']}\n纬度: {result['lat']}\n精准度: {result['precise']}")
            else:
                print(f"{address}: 查询失败，返回信息: {result['message']}")
        print()

def element_verification():
    while True:
        choice = input("请选择核验模式(0: 二要素核验, 1: 三要素核验, 输入exit退出): ")
        if choice.lower() == 'exit':
            break
        name = input("请输入姓名(输入exit退出): ")
        if name.lower() == 'exit':
            break
        id_card = input("请输入身份证号(输入exit退出): ")
        if id_card.lower() == 'exit':
            break
        if choice == '0':
            url = "https://hebcaonline.hebca.com/Hebca/interface/verifyPhoneNum.action"
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            data = {'verifyType': '102', 'personName': name, 'personIdcard': id_card, 'allCode': '20240430'}
            response = requests.post(url, headers=headers, data=data)
            result = response.json()
            if result.get('msg') == '认证通过' and result.get('status') == 1:
                print(f"二要素校验成功: {name} {id_card}")
            else:
                print(f"二要素校验失败: {name} {id_card}")
        elif choice == '1':
            phone_number = input("请输入手机号(输入exit退出): ")
            if phone_number.lower() == 'exit':
                break
            url = "https://hebcaonline.hebca.com/Hebca/interface/verifyPhoneNum.action"
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            data = {'verifyType': '106', 'personName': name, 'personIdcard': id_card, 'personMobile': phone_number, 'allCode': '20240430'}
            response = requests.post(url, headers=headers, data=data)
            result = response.json()
            if result.get('msg') == '认证通过' and result.get('status') == 1:
                print(f"三要素校验成功: {name} {id_card} {phone_number}")
            else:
                print(f"三要素校验失败: {name} {id_card} {phone_number}")
        else:
            print("无效的选择，请输入0或1。")
        print()

def qq_verification():
    while True:
        choice = input("请选择查询模式(0: QQ号查手机号, 1: 手机号查QQ号, 输入exit退出): ")
        if choice.lower() == 'exit':
            break
        if choice == '0':
            qq_number = input("请输入QQ号码(输入exit退出): ")
            if qq_number.lower() == 'exit':
                break
            url = f"https://zy.xywlapi.cc/qqapi?qq={qq_number}"
            result = request_with_retries(url)
            if 'error' in result:
                print(f"{qq_number}: 请求失败，错误信息: {result['error']}")
            else:
                phone = result.get('phone', '未知')
                phonediqu = result.get('phonediqu', '未知')
                print(f"QQ号码: {qq_number}\n手机号: {phone}\n归属地: {phonediqu}")
        elif choice == '1':
            phone_number = input("请输入手机号(输入exit退出): ")
            if phone_number.lower() == 'exit':
                break
            url = f"https://zy.xywlapi.cc/qqphone?phone={phone_number}"
            result = request_with_retries(url)
            if 'error' in result:
                print(f"{phone_number}: 请求失败，错误信息: {result['error']}")
            else:
                qq = result.get('qq', '未知')
                print(f"手机号: {phone_number}\nQQ号码: {qq}")
        else:
            print("无效的选择，请输入0或1。")
        print()

def generate_fake_residence():
    while True:
        name = input("请输入姓名(输入exit退出): ")
        if name.lower() == 'exit':
            break
        id_card = input("请输入身份证号(输入exit退出): ")
        if id_card.lower() == 'exit':
            break
        address = input("请输入地址(可选,回车跳过自动获取,输入exit退出): ")
        if address.lower() == 'exit':
            break
        host = base64.b64decode('MTcyLjIzMy41Ny4xMTI6ODA4MQ==').decode('utf-8')
        try:
            response = requests.get(f'http://{host}/jiahu?name={name}&id_card={id_card}&address={address}').json()
            print(response.get('msg'))
            if response.get('code') == 0:
                file_name = f'{name}-{id_card}.jpg'
                with open(file_name, 'wb') as f:
                    f.write(base64.b64decode(response.get('img')))
                print('已下载到本地')
                if sys.platform == "win32":
                    os.startfile(file_name)
                elif sys.platform == "darwin":
                    subprocess.call(["open", file_name])
                else:
                    subprocess.call(["xdg-open", file_name])
        except requests.RequestException as e:
            print(f"请求失败：{e}")

def wechat_query():
    while True:
        wechat_id = input("请输入要查询的微信名/微信号(输入exit退出): ")
        if wechat_id.lower() == 'exit':
            break
        url = f"http://jiansirc.top/api/wx/api.php?msg={wechat_id}&key=yongjiu66699"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{wechat_id}: 请求失败，错误信息: {result['error']}")
        else:
            if "数据未收录" in result:
                print(f"{wechat_id}: 查询失败，数据未收录")
            else:
                print(result.replace(',', '\n'))
        print()

def generate_phone_numbers():
    while True:
        qiansan = input("请输入手机号前三位(输入exit退出): ")
        if qiansan.lower() == 'exit':
            break
        houer = input("请输入手机号后二位: ")
        city = input("请输入城市: ")
        url = f"http://jiansirc.top/api/px/api.php?qiansan={qiansan}&houer={houer}&city={city}&type=text&key=yongjiu66699"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"请求失败，错误信息: {result['error']}")
        else:
            if "数据未收录" in result:
                print("查询失败，数据未收录")
            else:
                file_name = f"{qiansan}_{houer}_{city}_phones.txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"查询成功，结果已保存到 {file_name}")
                if os.name == 'nt':
                    os.startfile(file_name)
                elif os.name == 'posix':
                    subprocess.call(['open', file_name])
                else:
                    subprocess.call(['xdg-open', file_name])
        print()

def query_owner():
    while True:
        print("\n机主查询选项:")
        print("1. 破解机主")
        print("2. 四川机主")
        print("3. 北京机主")
        print("输入exit返回主菜单")
        choice = input("请选择查询类型: ")
        if choice.lower() == 'exit':
            break
        phone_number = input("请输入手机号(输入exit退出): ")
        if phone_number.lower() == 'exit':
            break
        if choice == '1':
            url = f"http://jiansirc.top/api/zyh/api.php?msg={phone_number}&key=yongjiu66699"
        elif choice == '2':
            url = f"http://jiansirc.top/api/scjz/api.php?msg={phone_number}&key=yongjiu66699"
        elif choice == '3':
            url = f"http://jiansirc.top/api/bjjz/api.php?msg={phone_number}&key=yongjiu66699"
        else:
            print("无效的选择，请重试。")
            continue
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{phone_number}: 请求失败，错误信息: {result['error']}")
        else:
            if "数据未收录" in result:
                print(f"{phone_number}: 查询失败，数据未收录")
            else:
                print(result.replace(',', '\n'))
        print()

def open_room_query():
    while True:
        name_or_hotel = input("请输入名字或酒店名字(输入exit退出): ")
        if name_or_hotel.lower() == 'exit':
            break
        url = f"http://jiansirc.top/api/kf/api.php?msg={name_or_hotel}&key=yongjiu66699"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{name_or_hotel}: 请求失败，错误信息: {result['error']}")
        else:
            if "数据未收录" in result:
                print(f"{name_or_hotel}: 查询失败，数据未收录")
            else:
                print(result.replace(',', '\n'))
        print()

def query_domain_info():
    while True:
        domain = input("请输入要查询的域名(输入exit退出): ")
        if domain.lower() == 'exit':
            break
        whois_url = f"https://www.yuanxiapi.cn/api/domain_whois/?domain={domain}"
        icp_url = f"https://www.yuanxiapi.cn/api/qqbeian/?url={domain}&type=JSON"
        whois_result = request_with_retries(whois_url)
        icp_result = request_with_retries(icp_url)
        if 'error' in whois_result:
            print(f"{domain}: WHOIS查询失败，错误信息: {whois_result['error']}")
        else:
            if whois_result['code'] == 200:
                print(f"域名: {whois_result['domain']}\n持有人: {whois_result['name']}\n持有人邮箱: {whois_result['email']}\nDNS服务器: {whois_result['dns']}\n注册商: {whois_result['registrars']}\n创建时间: {whois_result['Registration_Time']}\n过期时间: {whois_result['Expiration_Time']}")
            else:
                print(f"{domain}: WHOIS查询失败，返回信息: {whois_result['msg']}")
        if 'error' in icp_result:
            print(f"{domain}: ICP备案查询失败，错误信息: {icp_result['error']}")
        else:
            if icp_result['code'] == 200:
                print(f"域名: {icp_result['domain']}\nICP备案号: {icp_result['ICPSerial']}\n备案单位名称: {icp_result['Orgnization']}\n备案单位性质: {icp_result['natureName']}\n备案成功时间: {icp_result['pass_date']}\n备案网站名称: {icp_result.get('sitename', '无')}")
            else:
                print(f"{domain}: 未备案")
        print()

def query_port_scan():
    while True:
        ip = input("请输入要查询的IP或网站(输入exit退出): ")
        if ip.lower() == 'exit':
            break
        url = f"https://www.yuanxiapi.cn/api/port/?ip={ip}"
        result = request_with_retries(url)
        if 'error' in result:
            print(f"{ip}: 请求失败，错误信息: {result['error']}")
        else:
            if result['code'] == 200:
                ports = result['port']
                port_status = "\n".join([f"端口 {port}: {status}" for port, status in ports.items()])
                print(f"IP/网站: {result['host']}\n端口开放状态:\n{port_status}")
            else:
                print(f"{ip}: 查询失败，返回信息: {result['msg']}")
        print()

def scrape_website_source():
    while True:
        website_url = input("请输入要爬取的网站链接(输入exit退出): ")
        if website_url.lower() == 'exit':
            break
        ua_param = input("UA标识(留空则默认为百度UA): ")
        post_value_param = input("POST数据(可选): ")
        referer_param = input("自定义来源页referer(可选): ")
        params = {}
        if ua_param:
            params['ua'] = ua_param
        if post_value_param:
            params['post_value'] = post_value_param
        if referer_param:
            params['referer'] = referer_param
        url = f"https://www.yuanxiapi.cn/api/bazhan/?url={website_url}"
        result = request_with_retries(url, params=params)
        if 'error' in result:
            print(f"{website_url}: 请求失败，错误信息: {result['error']}")
        else:
            if result['code'] == 200:
                print(f"网站: {result['url']}\n压缩包下载链接: {result['zip']}\n效果示例链接: {result['yulan_url']}")
                download_choice = input("是否下载并打开压缩包？(y/n): ")
                if download_choice.lower() == 'y':
                    zip_url = result['zip']
                    zip_file = requests.get(zip_url)
                    zip_filename = f"{website_url.split('//')[1].replace('/', '_')}.zip"
                    with open(zip_filename, 'wb') as f:
                        f.write(zip_file.content)
                    print(f"压缩包已下载到 {zip_filename}")
                    if os.name == 'nt':
                        os.startfile(zip_filename)
                    elif os.name == 'posix':
                        subprocess.call(['open', zip_filename])
                    else:
                        subprocess.call(['xdg-open', zip_filename])
            else:
                print(f"{website_url}: 查询失败，返回信息: {result['code']}")
        print()

def main_menu():
    print("#############################")
    print("#                           #")
    print("#       冰块工具箱            #")
    print("#     (控制台0.14版本)        #")
    print("#                           #")
    print("#############################")
    print("作者: c0nt1n3n5al")
    print("说明：所有输入都可以使用空格分隔多个值。输入exit退出当前功能。")
    while True:
        print("\n功能选择:")
        print("0. 退出程序")
        print("1. 手机号归属地查询")
        print("2. IP定位查询")
        print("3. 地址经纬度查询")
        print("4. 二三要素验证")
        print("5. QQ号与手机号查询")
        print("6. 假户籍生成")
        print("7. 微信查询")
        print("8. 手机号跑现生成")
        print("9. 机主查询")
        print("10. 开房猎魔")
        print("11. 域名信息查询")
        print("12. 网站端口扫描")
        print("13. 在线爬取网站源码")
        choice = input("请选择一个功能: ")
        if choice == '0':
            break
        elif choice == '1':
            check_phone_location()
        elif choice == '2':
            check_ip_location()
        elif choice == '3':
            check_address_coordinates()
        elif choice == '4':
            element_verification()
        elif choice == '5':
            qq_verification()
        elif choice == '6':
            generate_fake_residence()
        elif choice == '7':
            wechat_query()
        elif choice == '8':
            generate_phone_numbers()
        elif choice == '9':
            query_owner()
        elif choice == '10':
            open_room_query()
        elif choice == '11':
            query_domain_info()
        elif choice == '12':
            query_port_scan()
        elif choice == '13':
            scrape_website_source()
        else:
            print("无效的选择，请重试。")

if __name__ == "__main__":
    main_menu()
