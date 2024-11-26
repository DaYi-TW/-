import schedule
import time
import requests
from bs4 import BeautifulSoup
import datetime
import random
from time import sleep

def 下班():
    # 只在星期一到星期五執行
    today = datetime.datetime.today().weekday()  # 0 是星期一，6 是星期日
    if today >= 0 and today <= 4:  # 星期一到星期五
        # Step 1: 先發送 GET 請求，獲取頁面內容及 cookies

        login_url = "https://cloud.nueip.com/login/"
        session = requests.Session()
        session.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        response = session.get(login_url)

        # Step 2: 提取 csrf_token 從 cookie 或頁面
        csrf_token = session.cookies.get('csrf_token')
        print(csrf_token)

        # get cookie
        session_cookie = requests.utils.dict_from_cookiejar(session.cookies)
        print(session_cookie)

        url = "https://cloud.nueip.com/login/index/param"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://portal.nueip.com",
            "referer": "https://portal.nueip.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        data = {
            "inputCompany": "64987355",
            "inputID": "00692",
            "inputPassword": "00692"
        }

        response = session.post(url, headers=headers, data=data)
        print(response.text)

        url = "https://cloud.nueip.com/home"
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到 <input name="token"> 的內容
        token_input = soup.find('input', {'name': 'token'})
        token_value = token_input.get('value') if token_input else None

        if token_value:
            print(f"Token: {token_value}")
        else:
            print("Token 未找到")
            return

        # 設定 N 的範圍（隨機選取的分鐘和秒數範圍）
        N_minutes = 5
        N_seconds = 59

        current_time = datetime.datetime.now()
        minutes_to_add = random.randint(0, N_minutes)
        seconds_to_add = random.randint(0, N_seconds)

        random_time = current_time + datetime.timedelta(minutes=minutes_to_add, seconds=seconds_to_add)
        random_time_str = random_time.strftime('%Y-%m-%d %H:%M:%S')

        print(random_time_str)

        url = "https://cloud.nueip.com/time_clocks/ajax"
        data = {
            "action": "add",
            "id": "2",
            "attendance_time": random_time_str,
            "token": token_value,
            "lat": "24.15066",
            "lng": "120.6625099"
        }
        sleep_second = random.randint(0, 10)
        sleep(sleep_second)
        response = session.post(url, headers=headers, data=data)

        print(response.text)

        return "下班打卡已完成"
    else:
        print("今天是週末，不執行打卡")

# 設定星期一到星期五晚上 18:00 執行
schedule.every().day.at("12:00").do(下班)

while True:
    schedule.run_pending()
    time.sleep(1)  # 每秒檢查一次排程
