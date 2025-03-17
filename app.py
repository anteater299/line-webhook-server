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

    if response.status_code != 200:
        print(f"❌ Push message failed: {response.text}")
        return {"error": response.text}

    message_count = len(messages)
    print(f"✅ Push message success: 發送 {message_count} 則訊息 | 回應: {response.json()}")
    return response.json()

# 產生 Carousel Template
def generate_carousel():
    sheet = get_google_sheet()
    data = sheet.get_all_records()[:10]  # 限制最多 10 筆資料
    columns = []
    
    for row in data:
        column = {
            "thumbnailImageUrl": row.get("image_url", ""),
            "title": row.get("title", "無標題"),
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

    if response.status_code != 200:
        print(f"❌ Reply message failed: {response.text}")
        return {"error": response.text}

    message_count = len(messages)
    print(f"✅ Reply message success: 發送 {message_count} 則訊息 | 回應: {response.json()}")
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Flask LINE Bot 使用 Google Sheets 運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received webhook data:", data)
    events = data.get("events", [])

    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            if user_message == "取得群組ID":
                group_id = event["source"].get("groupId", "無法取得群組 ID")
                reply_message(reply_token, [{"type": "text", "text": f"本群組 ID 為：\n{group_id}"}])
            
            elif user_message == "i划算早安":
                print("📢 Replying with carousel...")
                reply_message(reply_token, generate_carousel())

    return jsonify({"status": "success"})

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
