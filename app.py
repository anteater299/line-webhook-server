from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 你的 LINE Channel Access Token
LINE_ACCESS_TOKEN = "RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("收到的 Webhook 事件:", data)

    if "events" in data:
        for event in data["events"]:
            if event["type"] == "message" and "replyToken" in event:
                reply_token = event["replyToken"]
                send_carousel(reply_token)

    return jsonify({"status": "ok"})

def send_carousel(reply_token):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }

    body = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "template",
                "altText": "這是輪播訊息",
                "template": {
                    "type": "carousel",
                    "columns": [
                        {
                            "thumbnailImageUrl": "https://example.com/image1.jpg",
                            "title": "標題 1",
                            "text": "這是內容 1",
                            "actions": [
                                {"type": "message", "label": "按鈕 1", "text": "你點了 1"},
                                {"type": "uri", "label": "網站", "uri": "https://example.com"}
                            ]
                        },
                        {
                            "thumbnailImageUrl": "https://example.com/image2.jpg",
                            "title": "標題 2",
                            "text": "這是內容 2",
                            "actions": [
                                {"type": "message", "label": "按鈕 2", "text": "你點了 2"},
                                {"type": "uri", "label": "網站", "uri": "https://example.com"}
                            ]
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    print("回應結果:", response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
