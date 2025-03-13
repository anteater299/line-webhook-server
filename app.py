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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/357119_166928_A50A7951.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/447984_202232_0041E1A6.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/447971_202226_65F95E7C.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/445397_201025_ED5C7F70.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/442601_199996_8D6A0FE6.jpg",
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
                                    "thumbnailImageUrl": "https://openlife.7-11.com.tw/comm/ols/set/7ego2/item/432988_195847_9F706643.jpg",
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
