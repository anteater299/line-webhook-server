from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE Messaging API Token (請填入你的 Channel Access Token)
LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

def reply_message(reply_token, text):
    """發送回應給 LINE"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(LINE_REPLY_URL, headers=headers, json=data)

@app.route("/", methods=["GET"])
def home():
    return "Flask 伺服器運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    """處理 LINE Webhook 事件"""
    data = request.get_json()
    print("收到的 Webhook 事件:", data)  # 方便除錯，查看日誌

    events = data.get("events", [])
    for event in events:
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # 如果收到 "商品查詢"，則回應「收到」
            if user_message == "商品查詢":
                reply_message(reply_token, "收到")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

