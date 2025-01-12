import streamlit as st
import sqlite3
import time
import requests
from bs4 import BeautifulSoup
import datetime
import random
from time import sleep
import pandas as pd
import streamlit as st
import pandas as pd
import hydralit_components as hc
from streamlit_lottie import st_lottie
import requests
import json
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
# 檢查時間限制
def check_time(clock_in_type):
    now = datetime.now()
    hour, minute = now.hour, now.minute

    if clock_in_type == "上午打卡上班":
        return 7 <= hour < 8
    elif clock_in_type == "上午打卡下班":
        return 12 <= hour < 13
    elif clock_in_type == "下午打卡上班":
        return (hour == 12 and minute >= 0) or (hour == 13 and minute == 0)
    elif clock_in_type == "下午打卡下班":
        return 18 <= hour < 19
    return False


def 上班():
    today = datetime.today().weekday()
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
        current_time = datetime.now()
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
        # sleep(sleep_second)
        print(response.text)
        return "上班打卡已完成"
    else:
        print("Token 未找到")
        return

def 下班():
    today = datetime.today().weekday()
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
        current_time = datetime.now()
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
        # sleep(sleep_second)
        response = session.post(url, headers=headers, data=data)
        print(response.text)
        return "下班打卡已完成"
    else:
        print("Token 未找到")
        return


# 初始化 SQLite 資料庫
def init_db():
    conn = sqlite3.connect("attendance.db")  # 建立或連接到資料庫
    c = conn.cursor()
    # 建立打卡資料表
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            clock_in_type TEXT NOT NULL,
            clock_in_time TEXT NOT NULL
        )
    """)
    # 建立使用者帳號資料表
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    # 插入預設帳號（測試用）
    c.execute("""
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', '1234'), ('user1', 'password1')
    """)
    conn.commit()
    conn.close()

# 驗證使用者登入
def authenticate(username, password):
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# 新增打卡記錄
def add_record(username, clock_in_type):
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    clock_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO attendance (username, clock_in_type, clock_in_time)
        VALUES (?, ?, ?)
    """, (username, clock_in_type, clock_in_time))
    conn.commit()
    conn.close()

# 取得打卡記錄
def get_records():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM attendance ORDER BY clock_in_time DESC")
    records = c.fetchall()
    conn.close()
    return records



# 設置頁面配置
st.set_page_config(
    page_title="智慧打卡系統",
    page_icon="⏰",
    layout="wide",
)

# 自定義 CSS 樣式
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .success-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #dff0d8;
        border: 1px solid #d6e9c6;
        color: #3c763d;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f2dede;
        border: 1px solid #ebccd1;
        color: #a94442;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    # 初始化資料庫
    init_db()

    # 載入動畫
    lottie_clock = load_lottie_url('https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json')

    # 主標題區域
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col2:
            st.title("智慧員工打卡系統")
            st.markdown("#### 讓打卡變得更簡單、更智慧 ⚡")

    # 使用者登入區
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state.get("authenticated", False):
        # 創建登入卡片
        with st.container():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:

                # Provide unique keys for each text_input
                username = st.text_input("帳號", placeholder="請輸入帳號", key="username_input")
                password = st.text_input("密碼", placeholder="請輸入密碼", type="password", key="password_input")

                if st.button("登入系統", key="login_btn"):
                    if authenticate(username, password):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.success(f"歡迎回來，{username}！")
                        st.rerun()
                    else:
                        st.error("登入失敗！請檢查帳號或密碼。")

    else:
        # 顯示功能選單
        menu_data = [
            {'label': "打卡功能", 'icon': "✅"},
            {'label': "打卡記錄", 'icon': "📊"},
        ]
        
        with st.sidebar:
            st.success(f"👋 歡迎，{st.session_state['username']}")
            if st.button("登出系統", key="logout_btn"):
                st.session_state["authenticated"] = False
                st.rerun()

        # 主要功能區
        selected = hc.nav_bar(
            menu_definition=menu_data,
            override_theme={'txc_inactive': '#FFFFFF'},
            home_name='首頁',
            first_select=0
        )

        if selected == "打卡功能":
            st.write("### 今日打卡")
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                
                # 設定按鈕樣式
                button_style = """
                    <style>
                    div.stButton > button:first-child {
                        background-color: #4CAF50;
                        color: white;
                        height: 3em;
                        width: 100%;
                        border-radius: 10px;
                        border: none;
                        font-weight: bold;
                        margin: 0.5em 0;
                    }
                    </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)

                count = st_autorefresh(interval=1000, limit=None, key="autorefresh")
                current_time = datetime.now().strftime("%H:%M:%S")
                st.markdown(f"#### ⏰ 現在時間：{current_time}")

                with col1:
                    if st.button("上午打卡上班"):
                        if check_time("上午打卡上班"):
                            add_record(st.session_state["username"], "上午打卡上班")
                            st.success("✅ 上午打卡上班成功！")
                        else:
                            st.error("❌ 非打卡時段")

                with col2:
                    if st.button("上午打卡下班"):
                        if check_time("上午打卡下班"):
                            add_record(st.session_state["username"], "上午打卡下班")
                            st.success("✅ 上午打卡下班成功！")
                        else:
                            st.error("❌ 非打卡時段")

                with col3:
                    if st.button("下午打卡上班"):
                        if check_time("下午打卡上班"):
                            add_record(st.session_state["username"], "下午打卡上班")
                            st.success("✅ 下午打卡上班成功！")
                        else:
                            st.error("❌ 非打卡時段")

                with col4:
                    if st.button("下午打卡下班"):
                        if check_time("下午打卡下班"):
                            add_record(st.session_state["username"], "下午打卡下班")
                            st.success("✅ 下午打卡下班成功！")
                        else:
                            st.error("❌ 非打卡時段")

        elif selected == "打卡記錄":
            st.write("### 📊 打卡記錄查詢")
            records = get_records()
            if records:
                df = pd.DataFrame(records, columns=["ID", "使用者", "打卡類型", "打卡時間"])
                df = df.drop(columns=["ID"])
                df = df.reset_index(drop=True)
                
                # 使用 AgGrid 顯示表格
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("📝 目前尚無打卡記錄")

if __name__ == "__main__":
    main()



