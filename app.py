# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('7EgMow7uxowokDODkkKPAlCpBTHDiEonMBF3aRWVvDyWUe327qvsC9wiIJQpV7+zcrhQ5yVDxNNLy9gdDjNbDD+ZKudiHBVn0GXJfe0ic8jkLKVxCFW2/RHPVIjhlBWaSckrCxYafTe0rnBzl1p0fQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('4c3e800f2b2dd2c49b87326fc94a5357')

line_bot_api.push_message('Ud18701c20f39da291eeaba864d796ead', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個 function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('告訴我秘密', message):
        flex_message = TextSendMessage(
            text='請點選您想去的國家',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="日本", text="Japan")),
                QuickReplyButton(action=MessageAction(label="台灣", text="Taiwan")),
                QuickReplyButton(action=MessageAction(label="新加坡", text="Singapore")),
                QuickReplyButton(action=MessageAction(label="韓國", text="Korea")),
                QuickReplyButton(action=MessageAction(label="中國", text="China")),
                QuickReplyButton(action=MessageAction(label="美國", text="US"))
            ])
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('我想吃飯', message):
        flex_message = TextSendMessage(
            text='請選擇您想要的種類',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="主菜", text="主菜")),
                QuickReplyButton(action=MessageAction(label="湯品", text="湯品")),
                QuickReplyButton(action=MessageAction(label="飲料", text="飲料"))
            ])
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif message in ["主菜", "湯品", "飲料"]:
        response_message = TextSendMessage(text=f"您已成功將【{message}】加入購物車")
        line_bot_api.reply_message(event.reply_token, response_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入有效的指令"))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
