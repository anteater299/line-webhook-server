import requests
from flask import Flask, request

app = Flask(__name__)

LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
REPLY_URL = "https://api.line.me/v2/bot/message/reply"

def reply_message(reply_token, message_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [message_data]
    }
    requests.post(REPLY_URL, headers=headers, json=body)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    for event in data.get("events", []):
        if event["type"] == "message" and event["source"]["type"] == "group":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]

            if user_message == "查詢產品":
                carousel_template = {
                    "type": "template",
                    "altText": "群組 Carousel 多頁訊息",
                    "template": {
                        "type": "carousel",
                        "columns": [
                            {
                                "thumbnailImageUrl": "https://example.com/product1.jpg",
                                "title": "商品 A",
                                "text": "詳情內容",
                                "actions": [{"type": "uri", "label": "查看", "uri": "https://example.com"}]
                            },
                            {
                                "thumbnailImageUrl": "https://example.com/product2.jpg",
                                "title": "商品 B",
                                "text": "詳情內容",
                                "actions": [{"type": "uri", "label": "查看", "uri": "https://example.com"}]
                            }
                        ]
                    }
                }
                reply_message(reply_token, carousel_template)
            else:
                reply_message(reply_token, {"type": "text", "text": "請輸入正確查詢指令！"})

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
