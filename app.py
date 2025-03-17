from flask import Flask, request, jsonify
import requests
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# 讀取環境變數
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# 連接 Google Sheets，若不存在則建立
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_json:
        raise ValueError("找不到 GOOGLE_CREDENTIALS 環境變數")

    credentials_info = json.loads(credentials_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    try:
        return spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # 如果工作表不存在，則自動建立
        print(f"⚠️ 工作表 '{sheet_name}' 不存在，正在建立...")
        spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="10")
        return spreadsheet.worksheet(sheet_name)

# 記錄訊息發送結果
def log_message(sheet_name, message_type, recipient, status, response_text, group_member_count):
    sheet = get_google_sheet(sheet_name)
    import pytz
    timestamp = datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, message_type, recipient, status, response_text, group_member_count])

# 推送訊息 (Push API)
def push_message(to, messages):
    success_count = 0
    group_member_count = get_group_member_count(to)
    success_count = 0
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": to,
        "messages": messages
    }
    response = requests.post(LINE_PUSH_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        status = "成功"
        success_count = len(messages)
    status = "失敗"
    log_message("Push_Log", "PUSH", to, status, f"{response.text} | 成功發送 {success_count} 則訊息", group_member_count)
    
    return response.json()

# 產生 Carousel Template
def generate_carousel():
    sheet = get_google_sheet("Product_Data")
    data = sheet.get_all_records()[:10]  # 限制最多 10 筆資料
    columns = []
    
    for row in data:
        column = {
            "thumbnailImageUrl": row.get("image_url", ""),
            "title": str(row.get("title", "無標題"))[:40],  # 限制 40 字
            "text": str(row.get("price", "價格不詳"))[:60],  # 限制 60 字
            "actions": [
                {"type": "uri", "label": "查看商品", "uri": row.get("product_url", "#")}
            ]
        }
        columns.append(column)

    return [{
        "type": "template",
        "altText": "最新商品推薦",
        "template": {"type": "carousel", "columns": columns}
    }]

# 回應 LINE 訊息 (Reply API)
def reply_message(reply_token, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {"replyToken": reply_token, "messages": messages}
    response = requests.post(LINE_REPLY_URL, headers=headers, json=data)
    
    status = "成功" if response.status_code == 200 else "失敗"
    log_message("Reply_Log", "REPLY", reply_token, status, response.text)
    
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Flask LINE Bot 使用 Google Sheets 運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)  # 檢查 webhook 接收到的資料
    events = data.get("events", [])
    sheet = get_google_sheet("User_Input_Data")

    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]
            user_id = event["source"].get("userId", "未知")

            if user_message == "你好":
                reply_message(reply_token, [{"type": "text", "text": "請輸入日期(YYYY-MM-DD)和數字，以空格分隔"}])
            elif user_message == "i划算早安":
                reply_message(reply_token, generate_carousel())
            elif validate_input(user_message):
                date, number = user_message.split(" ")
                sheet.append_row([user_id, date, number])
                reply_message(reply_token, [{"type": "text", "text": f"已記錄: {date}, {number}"}])
            else:
                pass
    return jsonify({"status": "success"})

def validate_input(text):
    parts = text.split(" ")
    if len(parts) != 2:
        return False

    date, number = parts
    if not number.isdigit():
        return False

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False

    return True

@app.route("/push", methods=["POST"])
def send_push_message():
    """透過 Push API 推送多頁圖文訊息給多個群組"""
    data = request.get_json()
    group_ids = data.get("group_ids")  # 接收群組 ID 陣列

    if not group_ids or not isinstance(group_ids, list):
        return jsonify({"error": "缺少 group_ids 或格式錯誤"}), 400

    results = []
    for group_id in group_ids:
        push_result = push_message(group_id, generate_carousel())
        results.append({"group_id": group_id, "result": push_result})

    return jsonify(results)

def get_group_member_count(group_id):
    url = f"https://api.line.me/v2/bot/group/{group_id}/members/count"
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("count", "未知")
    return "未知"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
