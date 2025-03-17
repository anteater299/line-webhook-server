from flask import Flask, request, jsonify
import requests
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 讀取環境變數
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# 連接 Google Sheets
def get_google_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_json:
        raise ValueError("找不到 GOOGLE_CREDENTIALS 環境變數")

    credentials_info = json.loads(credentials_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)

# 記錄訊息發送結果
def log_message(sheet_name, message_type, recipient, status, response_text):
    sheet = get_google_sheet(sheet_name)
    sheet.append_row([message_type, recipient, status, response_text])

# 推送訊息 (Push API)
def push_message(to, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": to,
        "messages": messages
    }
    response = requests.post(LINE_PUSH_URL, headers=headers, json=data)

    status = "成功" if response.status_code == 200 else "失敗"
    log_message("Push_Log", "PUSH", to, status, response.text)
    
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Flask LINE Bot 使用 Google Sheets 運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received webhook data:", data)
    events = data.get("events", [])

    sheet = get_google_sheet("User_Input_Data")

    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]
            user_id = event["source"].get("userId", "未知")

            if user_message == "你好":
                reply_message(reply_token, [{"type": "text", "text": "請輸入日期(YYYY-MM-DD)和數字，以空格分隔"}])
            elif validate_input(user_message):
                date, number = user_message.split(" ")
                sheet.append_row([user_id, date, number])
                reply_message(reply_token, [{"type": "text", "text": f"已記錄: {date}, {number}"}])
            else:
                reply_message(reply_token, [{"type": "text", "text": "格式錯誤！請輸入 'YYYY-MM-DD 數字'"}])

    return jsonify({"status": "success"})

def validate_input(text):
    parts = text.split(" ")
    if len(parts) == 2:
        date, number = parts
        return date.count("-") == 2 and number.isdigit()
    return False

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
