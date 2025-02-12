from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def line_webhook():
    # 接收 LINE 的 Webhook JSON 資料
    data = request.json
    print("接收到的資料:", data)
    
    # 檢查是否有正確的事件格式
    if not data.get('events'):
        return jsonify({"status": "no events"})

    # 取得 reply token 和使用者訊息
    event = data['events'][0]
    if event['type'] == 'message' and event['message']['type'] == 'text':
        reply_token = event['replyToken']
        user_message = event['message']['text']

        # 建立回應訊息
        response = {
            "replyToken": reply_token,
            "messages": [
                {"type": "text", "text": f"你剛剛說了: {user_message}"}
            ]
        }

        return jsonify(response)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
