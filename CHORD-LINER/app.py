import os
from chalice import Chalice, Response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.exceptions import InvalidSignatureError

app = Chalice(app_name="chord-liner")

channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
channel_secret = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route('/callback', methods=['POST'])
def callback():
    signature = app.current_request.headers['X-Line-Signature']
    
    body = app.current_request.raw_body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        raise BadRequestError(e)
    return {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text != 'コード':
        return {}
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))