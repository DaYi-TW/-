import schedule
import time
import requests
from bs4 import BeautifulSoup
import datetime
import random
from time import sleep

def 上班():
    today = datetime.datetime.today().weekday()
    if today >= 0 and today <= 4:
        login_url = "https://cloud.nueip.com/login/"
        session = requests.Session()
        session.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        response = session.get(login_url)

        csrf_token = session.cookies.get('csrf_token')
        session_cookie = requests.utils.dict_from_cookiejar(session.cookies)

        url = "https://cloud.nueip.com/login/index/param"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://portal.nueip.com",
            "referer": "https://portal.nueip.com/",
            "user-agent": session.headers['user-agent'],
        }

        data = {
            "inputCompany": "64987355",
            "inputID": "00692",
            "inputPassword": "00692"
        }

        response = session.post(url, headers=headers, data=data)
        response = session.get("https://cloud.nueip.com/home")
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        token_value = token_input.get('value') if token_input else None

        if token_value:
            N_minutes = 2
            N_seconds = 59
            current_time = datetime.datetime.now()
            minutes_to_add = random.randint(0, N_minutes)
            seconds_to_add = random.randint(0, N_seconds)

            random_time = current_time + datetime.timedelta(minutes=minutes_to_add, seconds=seconds_to_add)
            random_time_str = random_time.strftime('%Y-%m-%d %H:%M:%S')

            url = "https://cloud.nueip.com/time_clocks/ajax"
            payload = {
                "action": "add",
                "id": "1",
                "token": token_value,
                "attendance_time": random_time_str,
                "lat": "24.15066",
                "lng": "120.6625099"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "accept": "application/json"
            }

            response = session.post(url, data=payload, headers=headers)
            sleep_second = random.randint(0, 10)
            sleep(sleep_second)
            print(response.text)
            return "上班打卡已完成"
        else:
            print("Token 未找到")
            return
    else:
        print("今天是週末，不執行打卡")

def 下班():
    today = datetime.datetime.today().weekday()
    if today >= 0 and today <= 4:
        login_url = "https://cloud.nueip.com/login/"
        session = requests.Session()
        session.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        response = session.get(login_url)

        csrf_token = session.cookies.get('csrf_token')
        session_cookie = requests.utils.dict_from_cookiejar(session.cookies)

        url = "https://cloud.nueip.com/login/index/param"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://portal.nueip.com",
            "referer": "https://portal.nueip.com/",
            "user-agent": session.headers['user-agent'],
        }

        data = {
            "inputCompany": "64987355",
            "inputID": "00692",
            "inputPassword": "00692"
        }

        response = session.post(url, headers=headers, data=data)
        response = session.get("https://cloud.nueip.com/home")
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        token_value = token_input.get('value') if token_input else None

        if token_value:
            N_minutes = 5
            N_seconds = 59
            current_time = datetime.datetime.now()
            minutes_to_add = random.randint(0, N_minutes)
            seconds_to_add = random.randint(0, N_seconds)

            random_time = current_time + datetime.timedelta(minutes=minutes_to_add, seconds=seconds_to_add)
            random_time_str = random_time.strftime('%Y-%m-%d %H:%M:%S')

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
            print("Token 未找到")
            return
    else:
        print("今天是週末，不執行打卡")

# 排程設定
schedule.every().day.at("08:55").do(上班)
schedule.every().day.at("12:00").do(下班)
schedule.every().day.at("12:50").do(上班)
schedule.every().day.at("18:00").do(下班)

while True:
    schedule.run_pending()
    time.sleep(1)
