Slack-namecard
===

Slackの任意のユーザの名札を作る

## 使い方

`slack_namecard.py [-t TOKEN] [-f FILE] [-u [USER [USER ...]]]`

* -t, --token: APIトークン
* -f, --file: 名札を作るユーザ(name)一覧ファイル
    * ファイルには1行1ユーザ(name)で記述していく
* -u, --user: 名札を作るユーザ(name)

上記コマンド入力後，
`{実行ファイルディレクトリ}/deriverable/{チーム名}/namecard/`配下に名札画像が生成され，
`{実行ファイルディレクトリ}/deliverable/{チーム名}/` 配下にpdfが生成される

* {チーム名}.pdf: 印刷用ファイル
* dummy.pdf: 白名札(ユーザのアイコン，名前等の情報なし)

## 実装できた
* Web APIからの情報取得
    * ユーザ情報(name,real\_name,icon)
    * チーム名，チームアイコン
* 名札画像生成
* ユーザリストファイルからの一括作成
* コマンドラインでのユーザ直接入力
* 印刷用pdf作成

## そのうち実装するかも
* 名札デザインのテンプレート選択
* 文字列が長かった場合の折り返し
* 要素配置の依存関係(他要素の配置から自己の配置を決める)

## 要求環境
* Python3 > 3.4
* [PyYAML](http://pyyaml.org/)
* [Wand](https://pypi.python.org/pypi/Wand) > 0.4.0
* [PyPDF2](https://github.com/mstamy2/PyPDF2)

## 動作確認
* Python 3.5.2
* PyYAML 3.12
* Wand 0.4.4
* PyPDF2 1.26

<!--
## ライセンス
そのうち考える
-->
