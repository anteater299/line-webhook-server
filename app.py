from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 設定你的 LINE 官方帳號 Channel Access Token
LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

# 商品資訊（可改為資料庫查詢）
PRODUCTS = [
    {
        "title": "📱 iPhone 15",
        "description": "最新 iPhone 15，A16 晶片，超高畫質相機。",
        "image_url": "https://example.com/iphone15.jpg",
        "product_url": "https://example.com/iphone15"
    },
    {
        "title": "💻 MacBook Pro 16",
        "description": "M3 晶片，16 吋 Retina 顯示器。",
        "image_url": "https://example.com/macbook16.jpg",
        "product_url": "https://example.com/macbook16"
    },
    {
        "title": "🎧 AirPods Pro",
        "description": "主動降噪、超長續航。",
        "image_url": "https://example.com/airpodspro.jpg",
        "product_url": "https://example.com/airpodspro"
    }
]

# Webhook 接收 LINE 事件
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("收到的 Webhook 事件:", data)

    if "events" in data:
        for event in data["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                user_message = event["message"]["text"].strip()  # 去除空格
                reply_token = event["replyToken"]

                # 如果使用者輸入「商品查詢」，回應 Carousel 訊息
                if user_message == "商品查詢":
                    send_carousel_message(reply_token)

    return jsonify({"status": "ok"})


# 送出 Carousel 訊息
def send_carousel_message(reply_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }

    # 建立多頁 Carousel 訊息
    carousel_columns = []
    for product in PRODUCTS:
        column = {
            "thumbnailImageUrl": product["image_url"],
            "title": product["title"],
            "text": product["description"],
            "actions": [
                {"type": "uri", "label": "查看商品", "uri": product["product_url"]}
            ]
        }
        carousel_columns.append(column)

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "template",
                "altText": "商品列表",
                "template": {
                    "type": "carousel",
                    "columns": carousel_columns
                }
            }
        ],
    }

    response = requests.post(LINE_REPLY_URL, headers=headers, json=payload)
    print("LINE 回應結果:", response.status_code, response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
