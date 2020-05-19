from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import dropbox
from dropbox.files import WriteMode
import datetime
import numpy as np
import math
app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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

def writing(words):
    dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
    dbx.users_get_current_account()
    dbx.files_download_to_file('/tmp/log.txt','/backup/backup.txt')
    now = datetime.datetime.now()
    with open("/tmp/log.txt","a") as f:
        f.write(words+'\t{0:%Y%m%d%H%M%S}\n'.format(now))
    with open('/tmp/log.txt', 'rb') as f:
        dbx.files_upload(f.read(),'/backup/backup.txt',mode=WriteMode('overwrite'))

def index(human_unit):
    if human_unit >= 1 * 10**int(math.log10(human_unit)) and human_unit < 2 * 10**int(math.log10(human_unit)) :
        MF = 0
    elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):
        MF = 1
    
    dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
    dbx.users_get_current_account()
    dbx.files_download_to_file('/tmp/kekka.csv','/backup/kekka.csv')
    raw_data = open("/tmp/kekka.csv", 'r')
    data = np.loadtxt(raw_data, delimiter=",")
    dd = data[np.where(data[:,MF] == human_unit)]
    raw_data.close()
    dd_sort = dd[np.argsort(dd[:, 2])[::-1]]
    #data = [[human_unit,0,human_unit + 10],[human_unit + 20,0,human_unit + 30]]
    return dd_sort

def poow(num):
    return num * num

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    human_unit = int(event.message.text) 
    dd = index(human_unit)
    words=""
    if human_unit < 2 * 10**int(math.log10(human_unit)) :
        FM = 1
    elif human_unit => 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):
        FM = 0
    for i in dd:
        words += str(str(int(i[FM]))+" → "+str(int(i[2]))+"\n")
    words = words.rstrip()
    #words = poow(int(event.message.text))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(words)))
    writing(event.message.text)

    


if __name__ == "__main__":
#    app.run()
    
    writing("hello")
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)