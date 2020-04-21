'''
Copyright © 2020 YutoWatanabe
'''
import os
import datetime

from json_operation import json_read, json_write


def format_report(save_directory: str, body: str) -> int:
    '''
    第何報かを返します。
    - 比較対象は前回のものから1h(3600s)
    - 本文が同じ内容だった場合に対してReturnが+1ずつ増加していきます

    Args:
        save_directory(str): ファイルを保存するディレクトリ
        body(str): 本文

    Returns:
        int: 第何報か
    '''
    save_file_path = os.path.join(save_directory, 'report.json')
    now = datetime.datetime.now()

    if os.path.isfile(save_file_path):
        previous_data = json_read(save_file_path)
    else:
        previous_data = []

    if previous_data != []:
        delete_data = []
        for index, element in enumerate(previous_data):
            date = datetime.datetime.strptime(str(element['date']), r'%Y%m%d%H%M%S')
            diff_date = now - date
            if diff_date.seconds > 3600:
                delete_data.append(index)

        for index in delete_data:
            del previous_data[index]

    is_existence = False
    for element in previous_data:
        if body == element['subject']:
            is_existence = True
            report = element['report']
            element['date'] = now.strftime(r'%Y%m%d%H%M%S')
            element['report'] += 1
            break
    if not is_existence:
        report = 1
        data = {
            'date': now.strftime(r'%Y%m%d%H%M%S'),
            'subject': body,
            'report': report
        }
        previous_data.append(data)

    json_write(save_file_path, previous_data)
    return report
