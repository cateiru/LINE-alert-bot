'''
Copyright © 2020 YutoWatanabe
'''
import re
from typing import Any


def apply_template(text: Any) -> Any:
    '''
    タイトルから適切なテンプレートを指定します。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    tsunami = re.search(r'津波', title)
    seismic_intensity_bulletin = re.search(r'震度速報', title)
    epicenter_and_seismic_intensity = re.search(r'震源・震度に関する情報', title)

    if seismic_intensity_bulletin:
        template = seismic_intensity_bulletin_template(text)
    elif title == '震源に関する情報':
        template = epicenter_information_template(text)
    elif epicenter_and_seismic_intensity:
        template = epicenter_and_seismic_intensity_template(text)
    elif title == '緊急地震速報（予報）':
        template = earthquake_early_warning_forecast_template(text)
    elif title == '緊急地震速報（警報）':
        template = earthquake_early_warning_alarm_template(text)
    elif tsunami:
        template = tsunami_template(text)
    else:
        template = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Error",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#fff77a",
                        "wrap": True
                    }
                ]
            },
            "styles": {
                "body": {
                    "backgroundColor": "#010101",
                    "separatorColor": "#010101"
                }
            }
        }

    return template


def seismic_intensity_bulletin_template(text: Any) -> Any:
    '''
    震度速報のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body, areas, info

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']
    areas = '\n'.join(text['areas'])
    info = text['info']

    template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#a30001",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": body,
                                    "wrap": True,
                                    "color": "#e0e0e0",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": areas,
                                    "wrap": True,
                                    "color": "#fff77a",
                                    "size": "md",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": info,
                                    "wrap": True,
                                    "color": "#e0e0e0"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#010101",
                "separatorColor": "#010101"
            }
        }
    }

    return template


def epicenter_information_template(text: Any) -> Any:
    '''
    震源に関する情報のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body, magnitude, area, info

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']
    magnitude = f'マグニチュード: M{text["magnitude"]}'
    area = f'震源地: {text["area"]}'
    info = text['info']

    template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#c4cf4c",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "color": "#e0e0e0",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": magnitude,
                            "color": "#fff77a",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": area,
                            "flex": 5,
                            "size": "sm",
                            "color": "#fff77a",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": info,
                            "color": "#e0e0e0",
                            "wrap": True,
                            "flex": 5
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#010101",
                "separatorColor": "#010101"
            }
        }
    }

    return template


def epicenter_and_seismic_intensity_template(text: Any) -> Any:
    '''
    震源・震度に関する情報のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body, magnitude, area, max_seismic_intensity, info

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']
    magnitude = f'マグニチュード: M{text["magnitude"]}'
    area = f'震源地: {text["area"]}'
    max_seismic_intensity = f'最大震度: 震度{text["max_seismic_intensity"]}'
    info = text['info']

    template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#c4cf4c",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "color": "#e0e0e0",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": magnitude,
                            "color": "#fff77a",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": area,
                            "flex": 5,
                            "size": "sm",
                            "color": "#fff77a",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": max_seismic_intensity,
                            "size": "sm",
                            "color": "#fff77a",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": info,
                            "color": "#e0e0e0",
                            "wrap": True,
                            "flex": 5
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#010101",
                "separatorColor": "#010101"
            }
        }
    }

    return template


def earthquake_early_warning_forecast_template(text: Any) -> Any:
    '''
    緊急地震速報(予報)のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']

    template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#a30001",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "color": "#e0e0e0",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#010101",
                "separatorColor": "#010101"
            }
        }
    }

    return template


def earthquake_early_warning_alarm_template(text: Any) -> Any:
    '''
    緊急地震速報(警報)のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']
    areas = '\n'.join(text['areas'])

    template = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#a30001",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "color": "#e0e0e0",
                            "size": "sm",
                            "flex": 5,
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": areas,
                            "flex": 5,
                            "wrap": True,
                            "color": "#fff77a"
                        }
                    ]
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#010101",
                "separatorColor": "#010101"
            }
        }
    }

    return template


def tsunami_template(text: Any) -> Any:
    '''
    津波情報のテンプレートを設定する。

    Args:
        text (Any): 送信するタイトルなどの情報が入ったDict
                    title, body, (area)

    Returns:
        Any: テンプレートを適用
    '''
    title = text['title']
    body = text['body']

    if 'area' in text:
        area = text['area']

        template = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#fff77a",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": body,
                                "color": "#e0e0e0",
                                "size": "sm",
                                "flex": 5,
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": area,
                                "color": "#010101"
                            }
                        ]
                    }
                ]
            },
            "styles": {
                "body": {
                    "backgroundColor": "#a30001",
                    "separatorColor": "#a30001"
                }
            }
        }
    else:
        template = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": "#fff77a",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": body,
                                "color": "#e0e0e0",
                                "size": "sm",
                                "flex": 5,
                                "wrap": True
                            }
                        ]
                    }
                ]
            },
            "styles": {
                "body": {
                    "backgroundColor": "#a30001",
                    "separatorColor": "#a30001"
                }
            }
        }

    return template
