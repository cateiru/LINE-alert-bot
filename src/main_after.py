'''
Copyright © 2020 YutoWatanabe
'''
import os
# import time
from typing import Any, Dict
import xmltodict

import click
import requests

from json_operation import json_read, json_write


@click.command()
@click.option('--line-token', 'token', prompt=True, hide_input=True, help='Line token')
def main():
    run_directory = os.path.dirname(__file__)
    url = 'http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml'
    earthquake = Earthquake(run_directory, url)
    while(True):
        if earthquake.check_update():
            earthquake.get_earthquake_information()


class Earthquake():
    def __init__(self, save_directory: str, url: str):
        self.url = url
        self.save_directory = save_directory
        self.directory = os.path.join(self.save_directory, 'saves')
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

        self.responce = None
        self.formated_text = []
        self.xml_root = None
        self.child = None

    def check_update(self) -> bool:
        '''
        サイトが更新されているか確認します。

        Returns:
            bool: 更新されていた場合True。されていない場合はFalse。
        '''
        is_update = False
        self.responce = requests.get(self.url)
        last_acquisition_file_path = os.path.join(self.directory, 'last_acquisition.json')
        last_acquisition = __load_buffer(last_acquisition_file_path, {'latest': None})

        last_modified = self.responce.headers['Last-Modified']

        if last_modified != last_acquisition['latest']:
            is_update = True
            __save_buffer(last_acquisition_file_path, {'latest': last_modified})

        return is_update

    def get_earthquake_information(self):
        '''
        地震速報を取得します。
        - 震度速報
        - 震源に関する情報
        - 震源・震度に関する情報
        - 緊急地震速報(予報)
        - 緊急地震速報(警報)

        すべてをフォーマットします。
        '''
        if self.responce is None:
            self.responce = requests.get(self.url)
        self.responce.encoding = 'UTF-8'
        text = self.responce.text

        self.xml_root = xmltodict.parse(text)
        for child in self.xml_root:
            title = child['entry']['title']
            if title == '震度速報':
                url = child['author']['link']
                self.__earthquake_intensity_report(url)
            elif title == '震源に関する情報':
                url = child['author']['link']
                self.__epicenter_information(url)
            elif title == '震源・震度に関する情報':
                url = child['author']['link']
                self.__information_on_epicenter_and_seismic_intensity(url)
            elif title == '緊急地震速報（予報）':
                url = child['author']['link']
                self.__earthquake_early_warning_forecast(url)
            elif title == '緊急地震速報（警報）':
                url = child['author']['link']
                self.__earthquake_early_warning_alarm(url)

    def __earthquake_intensity_report(self, url):
        '''
        フォーマット。
        -----
        【震度速報】
        ここにメイン文

        震度4: エリア1
        震度3: エリア2, エリア3, エリア4

        -----
        > 震度速報
        '''
        earthquake_details = __request_text(url)
        details_root = xmltodict.parse(earthquake_details)

        main_text = details_root['Report']['Head']['Headline']['Text']

        area_info = __format_area(details_root)

        text = f'【震度速報】\n{main_text}\n\n'
        for element in area_info:
            text += f'{element}: {area_info[element]}\n'
        self.formated_text.append(text)

    def __epicenter_information(self, url):
        '''
        フォーマット
        > 震源に関する情報
        '''
        # earthquake_details = __request_text(url)
        # details_root = xmltodict.parse(earthquake_details)
        text = '【震源に関する情報】'
        self.formated_text.append(text)

    def __information_on_epicenter_and_seismic_intensity(self, url):
        '''
        フォーマット
        -----
        【震源・震度に関する情報】
        ここにメイン文

        エリア: [エリア: str]

        マグニチュード: [マグニチュード: str]

        最大震度: [str]
        -----
        > 震源・震度に関する情報
        '''
        earthquake_details = __request_text(url)
        details_root = xmltodict.parse(earthquake_details)

        main_text = details_root['Report']['Head']['Headline']['Text']
        magnitude = details_root['Report']['Body']['Earthquake']['Hypocenter']['jmx_eb:Magnitude']
        area = details_root['Report']['Body']['Earthquake']['Hypocenter']['Area']['Name']
        max_seismic_intensity = ['Report']['Body']['Intensity']['Observation']['MaxInt']

        text = f'【震源・震度に関する情報】\n{main_text}\n\nエリア: {area}\n\nマグニチュード: M{magnitude}\n\n最大震度: {max_seismic_intensity}'
        self.formated_text.append(text)

    def __earthquake_early_warning_forecast(self, url):
        '''
        フォーマット
        > 緊急地震速報（予報）
        '''
        # earthquake_details = __request_text(url)
        # details_root = xmltodict.parse(earthquake_details)
        text = '【緊急地震速報 (予報)】'
        self.formated_text.append(text)

    def __earthquake_early_warning_alarm(self, url):
        '''
        フォーマット
        > 緊急地震速報（警報）
        '''
        # earthquake_details = __request_text(url)
        # details_root = xmltodict.parse(earthquake_details)
        text = '【緊急地震速報 (警報)】'
        self.formated_text.append(text)


def __format_area(details: Any) -> Dict[str, str]:
    '''
    震度とエリアの情報をフォーマットします。

    Args:
        details (Any): 元データ

    Returns:
        Dict[str, str]: フォーマットされたデータ。例: {'震度4': 'エリア1', '震度3': 'エリア2, エリア3, エリア4'}
    '''
    area_info = {}
    information = details['Report']['Head']['Headline']['Information'][0]['Item']
    if isinstance(information, list):
        for individual in information:
            seismic_intensity = individual['Kind']['Name']
            areas = []
            if isinstance(individual['Areas'], list):
                for area in individual['Areas']:
                    areas.append(area['Name'])
            else:
                areas.append(area['Name'])
            area_info[seismic_intensity] = ', '.join(areas)
    else:
        seismic_intensity = information['Kind']['Name']
        areas = []
        if isinstance(individual['Areas'], list):
            for area in individual['Areas']:
                areas.append(area['Name'])
        else:
            areas.append(area['Name'])
        area_info[seismic_intensity] = ', '.join(areas)

    return area_info


def __request_text(url: str) -> Any:
    '''
    リンクの内容を返します。

    Args:
        url (str): URL

    Returns:
        Any: 内容
    '''
    responce = requests.get(url)
    responce.encoding = 'UTF-8'
    return responce.text


def __load_buffer(path: str, empty_element: Any) -> Any:
    '''
    バッファファイルを読み込む。
    もし、新規でファイルを作成する場合はフォーマットを任意に決定します。

    Args:
        path (str): 読み込むファイルのパス
        empty_element (Any): ファイルを新規作成するときに読み込む内容。

    Returns:
        Any: バッファの内容。新規作成した場合は`empty_element`がそのまま返される。
    '''
    if os.path.isfile(path):
        buffer = json_read(path)
    else:
        buffer = empty_element

    return buffer


def __save_buffer(path: str, element: Any):
    '''
    バッファファイルを保存します。

    Args:
        path (str): 保存するファイルのパス
        element (Any): 保存する内容
    '''
    json_write(path, element)


if __name__ == "__main__":
    main()
