import boto3
from chalice import Chalice, Response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, AudioSendMessage
)
from linebot.exceptions import InvalidSignatureError
from chalicelib import chord_liner

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
    response = chord_liner.get_chord(event)
    if not response:
        return {}
    line_bot_api.reply_message(
        event.reply_token,
        AudioSendMessage(
            original_content_url=response['url'],
            duration=response['duration']
        ))