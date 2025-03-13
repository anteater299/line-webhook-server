from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 讀取環境變數中的 LINE Channel Access Token
LINE_ACCESS_TOKEN ="RZvVC1BJGeTbMX0ontVCsFsnaucBT2TtKo7wt44OWX7wdzGrgXRAuY0x2/djYdS7cdjI/UTHlZp9MskInhaRWTjYyeHYHXq5lEA63TQxHn5jhE8j/Nux+dJdEE47MX9IQkeiAcvvmAS5xbbT1DSs1QdB04t89/1O/w1cDnyilFU="
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
            "altText": "i划算推薦好康報你知",
            "template": {
                "type": "carousel",
                "columns": [
                   {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/347850_162769_973F20E6.jpg",
                                    "title": "【箱購】宏瑋80抽濕紙巾太厚駕到(40包入)",
                                    "text": "$888",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=bf36b596d203cbfb99a0"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463817_208602_7CBCD0A1.jpg",
                                    "title": "媽祖淨身除穢包10入",
                                    "text": "$148",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=dee137644ca851cba1f1"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463822_208603_59AD3AB1.jpg",
                                    "title": "Kinyo復刻3用輕巧掛脖扇-綠",
                                    "text": "$379",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=da3a44c773e6ad507005"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463824_208604_3ACB96ED.jpg",
                                    "title": "紅櫻花媽祖平安御守曲奇餅",
                                    "text": "$188",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=37d2a05d12e46913a85e"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463825_208605_D1A6C7A9.jpg",
                                    "title": "Kinyo復刻3用輕巧掛脖扇-粉",
                                    "text": "$379",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=49e9014248e4e40b882f"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463827_208606_843CF688.jpg",
                                    "title": "Kinyo復刻3用輕巧掛脖扇-白",
                                    "text": "$379",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=c742bc19203d445ea2c4"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/463827_208606_843CF688.jpg",
                                    "title": "Kinyo復刻3用輕巧掛脖扇-白",
                                    "text": "$379",
                                    "actions": [
                                        {
                                            "type": "uri",
                                            "label": "查看商品",
                                            "uri": "https://openlife.7-11.com.tw/comm/share/share.html?v=c742bc19203d445ea2c4"
                                        }
                                    ]
                                },
                                {
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/381549_178160_B8DA26E1.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/453119_204460_51316409.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/424486_193074_8385A54E.jpg",
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
