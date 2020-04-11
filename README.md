# LINE-alert-bot

![python](https://img.shields.io/github/pipenv/locked/python-version/yuto51942/LINE-alert-bot)
![last_commit](https://img.shields.io/github/last-commit/yuto51942/LINE-alert-bot)
<a href="https://lin.ee/jTUmGFn"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="20" border="0"></a>

 🇯🇵 |  [🇺🇸](doc/README_en.md)

<img src='doc/IMG_0128.png' width='400'>

## TL;DR

[気象庁から地震のデータ](http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml)を取得してLINEにpostします。

## 📢 送信する内容

- 震度速報
  - 本文、エリアごとの震度、注釈
- 震源・震度に関する情報
  - 本文、震源地、マグニチュード、最大震度、注釈
- 震源に関する情報
  - 本文、震源地、マグニチュード、注釈
- 緊急地震速報 (予報)
  - 本文
- 緊急地震速報 (警報)
  - 本文、エリア
- 津波予報
  - 本文
- 津波注意報
  - 本文、エリア
- 津波警報
  - 本文、エリア
- 大津波警報
  - 本文、エリア

## 💻 環境

- MacOS
- Ubuntu 18.04

Windowsは動作未確認

## ⚙ 依存関係のインストール

Pipenvからインストール

```bash
pip install pipenv

# pipenvの仮想環境上にインストール
pipenv install

# PC上にインストール
pipenv install --system --deploy
```

## 🚀 実行

<a href="https://lin.ee/jTUmGFn"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="20" border="0"></a>

```bash
# 実行
python src/main.py

# サーバー(Ubuntu)などで
nohup python3 src/main.py --line-token [token] &
```

## ✅ 静的解析

- Pylint
- mypy
- flake8

```bash
pipenv install --dev
pipenv shell
sh ./analysis.sh
```

## 📥 PRを出す際の注意点

- [静的解析](#✅-静的解析)をすべてクリアさせてください。
- Python DocstringをGoogleスタイル形式で記述してください。

## ⚖ ライセンス

[MIT License](LICENSE)
