import urllib3
import xmltodict
from typing import Dict


def access(url: str) -> str:
    '''
    URLからそのサイトの情報を取得します。

    Args:
        url ([type]): サイトのURL

    Returns:
        str: サイトの情報
    '''
    http = urllib3.PoolManager()
    request_body = http.request('GET', url)

    return request_body.data.decode('utf-8')


def convert_xml_to_dict(body: str) -> Dict:
    '''
    XML形式の情報をdictに変換する。

    Args:
        body (str): XMLのデータ

    Returns:
        Dict: Dict形式のデータ
    '''
    return xmltodict.parse(body)


if __name__ == "__main__":
    xml_body = access(url='http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml')
    print(convert_xml_to_dict(xml_body))
