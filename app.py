from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE Messaging API Token (請填入你的 Channel Access Token)
LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

def reply_message(reply_token, messages):
    """發送回應給 LINE"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_REPLY_URL, headers=headers, json=data)

@app.route("/", methods=["GET"])
def home():
    return "Flask 伺服器運行中"

@app.route("/webhook", methods=["POST"])
def webhook():
    """處理 LINE Webhook 事件"""
    data = request.get_json()
    print("收到的 Webhook 事件:", data)  # 確保你可以在日誌中看到這些訊息

    # 取得事件
    events = data.get("events", [])
    for event in events:
        # 確保事件為 message 並且為 text 類型
        if event.get("type") == "message" and event["message"].get("type") == "text":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # 如果收到 "商品查詢"，則回應多頁訊息
            if user_message == "商品查詢":
                carousel_template = [
                    {
                        "type": "template",
                        "altText": "這是商品查詢結果",
                        "template": {
                            "type": "carousel",
                            "columns": [
                                {
                                    "thumbnailImageUrl": "https://example.com/item1.jpg",
                                    "title": "(水果)日本青森葉乃果蘋果中果32規300g*6粒禮盒*2盒",
                                    "text": "好吃水果",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=e88a81727c47914204f9"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://example.com/item2.jpg",
                                    "title": "【UCC】 117精緻即溶咖啡-無糖2gx100入/盒",
                                    "text": "好喝咖啡",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=3f8f6735bbf59907f59b"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
                reply_message(reply_token, carousel_template)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

