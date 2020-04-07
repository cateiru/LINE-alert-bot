'''
test
'''
import os

from .json_operation import json_write
from .scrape import access, convert_xml_to_dict


def main():
    '''
    jsonに保存するテスト
    '''
    xml_data = access('http://www.data.jma.go.jp/developer/xml/data/2a2a4d94-45c2-3ef8-a4ba-a0860887e46f.xml')
    data = convert_xml_to_dict(xml_data)

    directory = os.path.dirname(__file__)
    save_fp = os.path.join(directory, 'test.json')
    json_write(save_fp, data)


if __name__ == "__main__":
    main()
