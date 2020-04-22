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
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "xxl",
                    "color": "#e9e8e8",
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "size": "md",
                            "color": "#e9e8e8",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xxl"
                        },
                        {
                            "type": "text",
                            "text": areas,
                            "size": "md",
                            "color": "#f4ce27",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "spacer",
                            "size": "lg"
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
                            "size": "md",
                            "color": "#e9e8e8",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "styles": {
            "header": {
                "backgroundColor": "#ef1925",
                "separatorColor": "#ef1925"
            },
            "body": {
                "backgroundColor": "#1c1c1c",
                "separatorColor": "#1c1c1c"
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
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "xl",
                    "color": "#1c1c1c",
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "size": "md",
                            "color": "#1c1c1c",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xxl"
                        },
                        {
                            "type": "text",
                            "text": area,
                            "size": "md",
                            "color": "#3b2feb",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": magnitude,
                            "size": "md",
                            "color": "#3b2feb",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "spacer",
                            "size": "lg"
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
                            "size": "md",
                            "color": "#1c1c1c",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "styles": {
            "header": {
                "backgroundColor": "#f0b80e",
                "separatorColor": "#ef1925"
            },
            "body": {
                "backgroundColor": "#e9e8e8",
                "separatorColor": "#1c1c1c"
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
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "xl",
                    "color": "#1c1c1c",
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "size": "md",
                            "color": "#1c1c1c",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xxl"
                        },
                        {
                            "type": "text",
                            "text": area,
                            "size": "md",
                            "color": "#3b2feb",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": magnitude,
                            "size": "md",
                            "color": "#3b2feb",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": max_seismic_intensity,
                            "size": "md",
                            "color": "#3b2feb",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "spacer",
                            "size": "lg"
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
                            "size": "md",
                            "color": "#1c1c1c",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "styles": {
            "header": {
                "backgroundColor": "#f0b80e",
                "separatorColor": "#ef1925"
            },
            "body": {
                "backgroundColor": "#e9e8e8",
                "separatorColor": "#1c1c1c"
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
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "xl",
                    "color": "#ef1925",
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "size": "md",
                            "color": "#e9e8e8",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "styles": {
            "header": {
                "backgroundColor": "#000000",
                "separatorColor": "#000000"
            },
            "body": {
                "backgroundColor": "#1c1c1c",
                "separatorColor": "#1c1c1c"
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
    areas = '、'.join(text['areas'])

    template = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "xl",
                    "color": "#ef1925",
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": body,
                            "size": "md",
                            "color": "#e9e8e8",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "xxl"
                        },
                        {
                            "type": "text",
                            "size": "md",
                            "color": "#f4ce27",
                            "weight": "bold",
                            "wrap": True,
                            "text": areas
                        },
                        {
                            "type": "spacer",
                            "size": "lg"
                        }
                    ]
                }
            ]
        },
        "styles": {
            "header": {
                "backgroundColor": "#000000",
                "separatorColor": "#000000"
            },
            "body": {
                "backgroundColor": "#1c1c1c",
                "separatorColor": "#1c1c1c"
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
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "size": "xl",
                        "color": "#ef1925",
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": body,
                                "size": "md",
                                "color": "#e9e8e8",
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "spacer",
                                "size": "xxl"
                            },
                            {
                                "type": "text",
                                "text": area,
                                "size": "md",
                                "color": "#f4ce27",
                                "weight": "bold"
                            },
                            {
                                "type": "spacer",
                                "size": "lg"
                            }
                        ]
                    }
                ]
            },
            "styles": {
                "header": {
                    "backgroundColor": "#223ba1",
                    "separatorColor": "#223ba1"
                },
                "body": {
                    "backgroundColor": "#1c1c1c",
                    "separatorColor": "#1c1c1c"
                }
            }
        }
    else:
        template = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "size": "xl",
                        "color": "#ef1925",
                        "weight": "bold",
                        "align": "center",
                        "wrap": True
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": body,
                                "size": "md",
                                "color": "#e9e8e8",
                                "wrap": True
                            }
                        ]
                    }
                ]
            },
            "styles": {
                "header": {
                    "backgroundColor": "#223ba1",
                    "separatorColor": "#223ba1"
                },
                "body": {
                    "backgroundColor": "#1c1c1c",
                    "separatorColor": "#1c1c1c"
                }
            }
        }

    return template
