import os
import boto3
from chalice import Chalice, Response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.exceptions import InvalidSignatureError

client = boto3.client('ssm')
parameters = client.get_parameters(
    Names = [
        'LINE_CHANNEL_ACCESS_TOKEN',
        'LINE_CHANNEL_SECRET'
    ],
    WithDecryption=True)
CHANNEL_ACCESS_TOKEN = parameters['Parameters'][0]['Value']
CHANNEL_SECRET = parameters['Parameters'][1]['Value']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Chalice(app_name="chord-liner")

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