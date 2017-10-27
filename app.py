# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the 'License'); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
# Google API Key: AIzaSyCgrAXdRBBTzDGjVfyALtpxBuocTZ_6XZ4
from __future__ import unicode_literals

import os
import sys
#import googlemaps
#import pyrebase
#import hashlib
import requests

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

tenor_json_api = 'https://api.tenor.com/v1/search?key=68WANYPCQ8AD'

# get channel_secret and channel_access_token from your environment variable
channel_secret = '68175c7954aae7473a6cd8cdff7c9eb8'
channel_access_token = 'XQJoytN7GaCaho0bPo/RX6EQ/zR5fGDEGiizH7PKTNkZix+LcIy5XXXB4/69+IdTUUcMQPXcfYyGOmZWrm8qiaWQGQ4rxK7ZQkDpSoeI8G/u0RY6RaZ7ExjPtu9n8hnkn6qGjz9Z5Ww42pctPxcO5AdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                if event.message.text.find('.gif') != -1:
                #ECHO MESSAGE CODE
                    query_text = event.message.text[:event.message.text.find('.gif')]
                
                    result = requests.get(tenor_json_api + '&q=' + query_text + '&limit=5&locale=zh_TW')
                
                    line_bot_api.push_message(
                        event.source.sender_id,
                        ImageSendMessage(
                            original_content_url=(result.json())['results'][0]['media'][0]['gif']['url'],
                            preview_image_url=(result.json())['results'][0]['media'][0]['gif']['preview']
                        )
                    )
        elif isinstance(event, JoinEvent):
            print 'GET JOIN REQUEST!'
            line_bot_api.push_message(
                event.source.sender_id,
                TextSendMessage(text='汪汪，輸入＿＿.gif獲得支援')
            )

    return 'OK'

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug)
