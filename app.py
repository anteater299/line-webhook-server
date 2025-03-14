from flask import Flask, request, jsonify
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

app = Flask(__name__)

# 讀取環境變數中的 LINE Channel Access Token
LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
GOOGLE_SHEET_ID = "1YWkpL5XubmUliraB2W0VcnoqaD8IaeMs6pzlhrxwrws" # 你的 Google Sheets ID
GOOGLE_API_KEY = "AIzaSyCCuxbwvxT_FGJ1zq3R4_jtMtcVgtI_sjg" # 你的 Google API Key

# 回應 LINE Bot 訊息
def reply_message(reply_token, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {"replyToken": reply_token, "messages": messages}
    return requests.post(LINE_REPLY_URL, headers=headers, json=data).json()

def push_message(to, messages):
    """使用 Push API 主動推送多頁圖文訊息"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": to,
        "messages": messages
    }
    response = requests.post(LINE_PUSH_URL, headers=headers, json=data)
    return response.json()

# 連接 Google Sheets
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).sheet1

# 產生 Carousel Template
def generate_carousel():
    sheet = get_google_sheet()
    data = sheet.get_all_records()  # 取得所有資料
    columns = [{
        "thumbnailImageUrl": row["image_url"],
        "title": row["title"],
        "text": row["price"],
        "actions": [{"type": "uri", "label": "查看商品", "uri": row["product_url"]}]
    } for row in data]

    return [{"type": "template", "altText": "最新商品推薦", "template": {"type": "carousel", "columns": columns}}]

@app.route("/", methods=["GET"])
def home():
    return "Flask 伺服器運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    """處理 LINE Webhook 事件"""
    data = request.get_json()
    print("收到的 Webhook 事件:", json.dumps(data, indent=2, ensure_ascii=False))

    events = data.get("events", [])
    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # 檢查是否來自群組
            if "source" in event and event["source"].get("type") == "group":
                group_id = event["source"]["groupId"]

                # 如果使用者輸入 "取得群組ID"，回應群組 ID
                if user_message == "取得群組ID":
                    reply_message(reply_token, [ {"type": "text", "text": f"本群組 ID 為：\n{group_id}"} ])

                # 如果使用者輸入 "商品查詢"，回應多頁圖文訊息
                elif user_message == "i划算早安":
                    reply_message(reply_token, generate_carousel())

    return jsonify({"status": "ignored"})  # 其他訊息不處理

@app.route("/push", methods=["POST"])
def send_push_message():
    """透過 Push API 推送多頁圖文訊息"""
    data = request.get_json()
    group_id = data.get("group_id")  # 群組 ID
    if not group_id:
        return jsonify({"error": "缺少 group_id"}), 400

    result = push_message(group_id, generate_carousel())
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
