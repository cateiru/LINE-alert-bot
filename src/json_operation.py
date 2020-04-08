'''
jsonファイルの操作をします。
'''
import json
from typing import Any


def json_read(json_file_path: str) -> Any:
    '''
    JSONファイルを読み込む

    Args:
        json_file_path (str): JSONファイルのパス

    Returns:
        Any: JSONの内容
    '''
    with open(json_file_path, mode='r') as contents:
        json_body = json.load(contents)

    return json_body


def json_write(json_file_path: str, json_body: Any) -> None:
    '''
    JSONを保存する。

    Args:
        json_file_path (str): JSONファイルパス
        json_body (Any): JSONの内容
    '''
    with open(json_file_path, mode='w') as contents:
        json.dump(json_body, contents, indent=4, ensure_ascii=False)
