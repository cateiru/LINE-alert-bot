# LINE-alert-bot

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/LINE-alert-bot)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/LINE-alert-bot)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/yuto51942/LINE-alert-bot/?ref=repository-badge)
<a href="https://lin.ee/jTUmGFn"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="20" border="0"></a>

 [🇯🇵](../README.md) |  🇺🇸

<img src='IMG_0128.png' width='400'>

## TL;DR

[We get earthquake data from the Japan Meteorological Agency](http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml) and post it to LINE.

## 📢 Contents to be sent

|                                    name                                     | content                                                           |
| :-------------------------------------------------------------------------: | :---------------------------------------------------------------- |
|               震度速報 (preliminary seismic intensity report)               | body, seismic intensity by area, notes                            |
| 震源・震度に関する情報 (Information on the epicenter and seismic intensity) | body, epicenter, magnitude, maximum seismic intensity, annotation |
|             震源に関する情報 (Information about the epicenter)              | body, epicenter, magnitude, annotation                            |
|          緊急地震速報 (予報) (Earthquake Early Warning (Forecast))          | body                                                              |
|          緊急地震速報 (警報) (Emergency Earthquake Alert (Alert))           | body, area                                                        |
|                        津波予報 (Tsunami to report)                         | body                                                              |
|                          津波注意報 (Tsunami note)                          | body, area                                                        |
|                          津波警報 (Tsunami alert)                           | body, area                                                        |
|                     大津波警報 (Major tsunami warning)                      | body, area                                                        |

## 💻 Environment

- Mac OS
- Ubuntu 18.04

Windows has not been tested.

## ⚙ Installing dependencies

Install from Pipenv.

```bash
pip install pipenv

# Install on the pipenv virtual environment
pipenv install

# Install on your PC
pipenv install --system --deploy
```

## 🚀 Run

<a href="https://lin.ee/jTUmGFn"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="20" border="0"></a>

```bash
# Run
python src/main.py

# Run on a server (Ubuntu), etc.
nohup python3 src/main.py --line-token [token] &
```

## ✅ Static analysis

- Pylint
- mypy
- flake8

```bash
pipenv install --dev
pipenv shell
sh ./analysis.sh
```

## 📥  Points to note when issuing a PR

- Clear all [static analysis](#-Static-analysis).
- Write the Python Docstring in Google style format.

## ⚖ LICENSE

[MIT License](..LICENSE)
