'''
Copyright © 2020 YutoWatanabe
'''
import sys
from typing import Any

import linebot
from linebot.models import TextSendMessage


def stop(messages: Any, line_bot_api: linebot.LineBotApi):
    '''
    震度7を観測した場合、システムの動作を停止する。
    震源・震度に関する情報の最大震度を取得する。
    (通信網のパンクを防ぐため)

    Args:
        messages(Any): フォーマットしていない送信する内容。複数の内容がある。
        line_bot_api: LINE API

    '''
    for message in messages:
        if 'max_seismic_intensity' in message:
            if message['max_seismic_intensity'] == '7':
                text = '''【システム一時停止のおしらせ】

先程、震度7を観測したためネットワークの混雑を避けるために「地震情報・速報」のサービスを一時停止いたします。

詳しい地震情報につきましては、「Yahoo!防災」「NERV防災」などのサービスをご利用ください。

災害時には情報を過信しすぎず周りの状況を見て行動してください。'''

                line_bot_api.broadcast(TextSendMessage(text=text))
                sys.exit('The operation was stopped normally because of the seismic intensity 7 was observed.')
