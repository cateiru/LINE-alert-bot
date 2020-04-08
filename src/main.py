'''
main
'''
import json
import os
import time
from xml.etree import ElementTree
from typing import Any, List

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
    while(True):  # pylint: disable=C0325
        connect(json_save_directory, token)
        time.sleep(30)


def connect(json_save_directory: str, token: str) -> None:
    '''
    情報を取得、フォーマット、LINEにpostを実行します。

    Args:
        json_file_path (str): JSONファイルのパス
        token (str): LINEのアクセストークン
    '''
    json_file_path = os.path.join(json_save_directory, 'save_alert.json')
    backup_path = os.path.join(json_save_directory, 'backup.json')

    xml_body = access('http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml')
    body = ElementTree.fromstring(xml_body)
    body = body.feed.entry

    if os.path.isfile(json_file_path):
        old_body = json_read(json_file_path)
    else:
        old_body = []

    if os.path.isfile(backup_path):
        backup_body = json_read(backup_path)
    else:
        backup_body = []

    new_alert = get_new_alert(body, old_body)
    json_write(json_file_path, body)
    if new_alert != [] and new_alert not in backup_body:
        new_alert = select_earthquake(new_alert)
        new_alert = format_text(new_alert)
        post_line(token, new_alert)
        print(f'POST:\n{new_alert}')
        backup_body += new_alert
        json_write(backup_path, backup_body)


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
        is_earthquake = ['震源・震度に関する情報', '震度速報', '震源に関する情報']
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

        try:
            if title == '震度速報':
                message = earthquake_early_warning(details_data)
            else:
                message = earthquake_information(details_data, title)
        except Exception:
            message = f'【format error】\n{json.dumps(details_data)}'

        text.append(message)
    return text


def earthquake_early_warning(details_data: Any) -> str:
    '''
    地震速報をフォーマットする。

    Args:
        details_data (Any): Dictのデータ

    Returns:
        str: 整形されたデータ
    '''
    main_message = details_data['Report']['Head']['Headline']['Text']
    seismic_intensity = details_data['Report']['Head']['Headline']['Information']['Item']['Kind']['Name']
    areas = details_data['Report']['Head']['Headline']['Information']['Item']['Areas']['Area']
    if isinstance(areas, list):
        area = areas[0]['Name']
        areas = areas[1:]
        for area_type in areas:
            area = f'{area}, {area_type["Name"]}'
    else:
        area = areas['Name']
    return f'【地震速報】\n{main_message}\n\n{seismic_intensity}: {area}'


def earthquake_information(details_data: Any, title: str) -> str:
    '''
    地震情報をフォーマットする

    Args:
        details_data (Any): Dictのデータ
        title (str): タイトル

    Returns:
        str: 整形されたデータ
    '''
    main_message = details_data['Report']['Head']['Headline']['Text']
    area = details_data['Report']['Body']['Earthquake']['Hypocenter']['Area']['Name']
    magnitude = details_data['Report']['Body']['Earthquake']['jmx_eb:Magnitude']['#text']
    comment = details_data['Report']['Body']['Comments']['ForecastComment']['Text']

    return f'【{title}】\n{main_message}\
\n---------\nエリア: {area}\n\nマグニチュード: M{magnitude}\n\n{comment}'


if __name__ == "__main__":
    main()  # pylint: disable=E1120
