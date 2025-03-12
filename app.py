from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# 讀取環境變數中的 LINE Channel Access Token
LINE_ACCESS_TOKEN = os.getenv("RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU=")
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

def reply_message(reply_token, messages):
    """使用 Reply API 回應多頁圖文訊息"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": messages
    }
    response = requests.post(LINE_REPLY_URL, headers=headers, json=data)
    return response.json()

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

def generate_carousel():
    """產生多頁圖文訊息（Carousel Template）"""
    return [
        {
            "type": "template",
            "altText": "這是多頁圖文訊息",
            "template": {
                "type": "carousel",
                "columns": [
                   {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/198284/image/MAI_174423644_X700X700.jpg",
                                    "title": "(水果)日本青森葉乃果蘋果中果32規300g*6粒禮盒*2盒",
                                    "text": "$2888",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=e88a81727c47914204f9"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/166928/image/MAI_154734938_X700X700.jpg",
                                    "title": "【韓國innisfree】無油無慮礦物控油蜜粉5g [買1送1]",
                                    "text": "$458",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=28fee610fa12a55b9ad6"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/202232/image/MAI_192711319_X700X700.jpg",
                                    "title": "米樂爆米花- 史努比花季寫生罐爆米花(10入/箱)-焦糖",
                                    "text": "$1780",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=ad5cda379f38a0d8b866"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/202226/image/MAI_183454795_X400X400.jpg?uts=175802593",
                                    "title": "【超比食品】燕麥脆片-微甜草莓x6包(100g/包)",
                                    "text": "$699",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=37d2a05d12e46913a85e"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/201025/image/MAI_111508012_X400X400.jpg?uts=175802593",
                                    "title": "時髦的安吉小姐 可微波陶瓷碗(黃/白) 含蓋",
                                    "text": "$249",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=634f8d8e1425dc761bb6"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/199996/image/MAI_152944914_X400X400.jpg?uts=175802593",
                                    "title": "寶可夢手提燜燒罐(三色選)",
                                    "text": "$593",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=85141b1306c58b63288d"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/195847/image/MAI_153641158_X400X400.jpg?uts=175802593",
                                    "title": "【利捷維】有酵超級B群膜衣錠 60錠",
                                    "text": "$429",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=aae26f7afe62d7df4719"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/178160/image/MAI_171909057_X400X400.png?uts=175802593",
                                    "title": "【羅技 Logitech】Pebble 2 Combo 無線藍芽 鍵盤滑鼠組",
                                    "text": "$1,790",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=af996c2aa30334fe9e30"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/198284/image/MAI_174423644_X700X700.jpg",
                                    "title": "(水果)日本青森葉乃果蘋果中果32規300g*6粒禮盒*2盒",
                                    "text": "$2888",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=e88a81727c47914204f9"
                                        }
                                    ]
                                },                                                           
                                {
                                    "thumbnailImageUrl": "https://711go.7-11.com.tw/Files/market/193074/image/MAI_134443667_X700X700.jpg",
                                    "title": "【UCC】 117精緻即溶咖啡-無糖2gx100入/盒",
                                    "text": "$499",
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
                elif user_message == "商品查詢":
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
