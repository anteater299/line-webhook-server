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
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# 連接 Google Sheets
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_json:
        raise ValueError("找不到 GOOGLE_CREDENTIALS 環境變數")

    credentials_info = json.loads(credentials_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).sheet1

# 產生 Carousel Template
def generate_carousel():
    sheet = get_google_sheet()
    data = sheet.get_all_records()[:10]  # 限制最多 10 筆資料
    print("Data from Google Sheets:", data)  # 檢查取得的資料
    columns = []
    
    for row in data:
        column = {
            "thumbnailImageUrl": row.get("image_url", ""),
            "title": row.get("title", "無標題"),
            "text": row.get("price", "價格不詳"),
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

# 回應 LINE Bot 訊息
def reply_message(reply_token, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {"replyToken": reply_token, "messages": messages}
    return requests.post(LINE_REPLY_URL, headers=headers, json=data).json()

@app.route("/", methods=["GET"])
def home():
    return "Flask LINE Bot 使用 Google Sheets 運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    events = data.get("events", [])
    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            if user_message == "i划算早安":
                reply_message(reply_token, generate_carousel())

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
