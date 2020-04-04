'''
main
'''
import os
import re
import time
from typing import List, Any

import click
import linebot
from linebot.models import TextSendMessage

from json_operation import json_read, json_write
from scrape import access, convert_xml_to_dict


@click.command()
@click.option('--line-token', 'token', prompt=True, hide_input=True, help='LINE webhook.')
def main(token: str) -> None:
    '''
    メイン

    Args:
        token (str): LINEのアクセストークン
    '''
    directory = os.path.dirname(__file__)
    json_save_directory = os.path.join(directory, 'json_save')
    if not os.path.isdir(json_save_directory):
        os.makedirs(json_save_directory)
    json_file_path = os.path.join(json_save_directory, 'save_alert.json')
    while(True):  # pylint: disable=C0325
        connect(json_file_path, token)
        time.sleep(1)


def connect(json_file_path: str, token: str) -> None:
    '''
    情報を取得、フォーマット、LINEにpostを実行します。

    Args:
        json_file_path (str): JSONファイルのパス
        token (str): LINEのアクセストークン
    '''
    xml_body = access('http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml')
    json_body = convert_xml_to_dict(xml_body)
    body = json_body['feed']['entry']

    if os.path.isfile(json_file_path):
        old_body = json_read(json_file_path)
    else:
        old_body = []
    new_alert = get_new_alert(body, old_body)
    json_write(json_file_path, body)
    if new_alert != []:
        new_alert = select_earthquake(new_alert)
        new_alert = format_text(new_alert)
        post_line(token, new_alert)
        print(f'POST:\n{new_alert}')


def post_line(token: str, text: List[str]):
    '''
    LINE BOTにpostします。

    Args:
        token (str): LINEのアクセストークン
        text (str): 送信するメッセージ
    '''
    line_bot_api = linebot.LineBotApi(token)
    for message in reversed(text):
        line_bot_api.broadcast(TextSendMessage(text=message))


def get_new_alert(body: Any, old_body: Any):
    '''
    古い情報を取得して新しい情報が取得された際にそれを返す。

    Args:
        body (Any): 新しいデータ
        old_body (Any): 古いデータ
    '''
    new_alert = []
    for element in body:
        if element not in old_body:
            new_alert.append(element)
        else:
            break
    return new_alert


def select_earthquake(body: Any) -> Any:
    '''
    地震に関する情報のみ取得

    Args:
        body (Any): 情報

    Returns:
        Any: 地震に関する情報
    '''
    earthquake_data = []
    for element in body:
        is_earthquake = re.match(r'震', element['title'])
        if is_earthquake:
            earthquake_data.append(element)
    return earthquake_data


def format_text(body: Any) -> List[str]:
    '''
    SNSなどに投稿できるようにフォーマットします。

    Args:
        body (Any): 取得したデータ

    Returns:
        List[str]: フォーマットしたデータ
    '''
    text = []
    for element in body:
        link = element['link']['@href']
        xml_details_data = access(link)
        details_data = convert_xml_to_dict(xml_details_data)

        title = details_data['Report']['Head']['Title']

        if title == '震度速報':
            main_message = details_data['Report']['Head']['Headline']['Text']
            seismic_intensity = details_data['Report']['Head']['Headline']['Information']['Item']['Kind']['Name']
            area = details_data['Report']['Head']['Headline']['Information']['Item']['Areas']['Area']['Name']
            message = f'【地震速報】\n{main_message}\n\n{seismic_intensity}: {area}'
        else:
            target_time = details_data['Report']['Head']['TargetDateTime']
            main_message = details_data['Report']['Head']['Headline']['Text']
            area = details_data['Report']['Body']['Earthquake']['Hypocenter']['Area']['Name']
            magnitude = details_data['Report']['Body']['Earthquake']['jmx_eb:Magnitude']['#text']
            comment = details_data['Report']['Body']['Comments']['ForecastComment']['Text']

            message = f'【{title}】\n発生時間: {target_time}\n{main_message}\
\n---------\nエリア: {area}\n\nマグニチュード: M{magnitude}\n\n{comment}'
        text.append(message)
    return text


if __name__ == "__main__":
    main()  # pylint: disable=E1120
