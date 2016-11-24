# vrrc
VRラジコン用

# ライブラリinstallについて
1. requirements.txtにライブラリ名==バージョン の行を足す
2. pip install -r requirements.txt

# websocket
URI: ws://172.16.2.159:9090/ws
Chromeのwebsocketお試しplugin を使うとテストしやすい
https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo

# websocket message format
JSON。
command&valueの配列を垂れ流しで送信

例：
```
[
  {
    "command": "steering",
    "value": 35
  },
  {
    "command": "acceralation",
    "value": 20
  },
  {
    "command": "steering",
    "value": 37
  },
  ...
]
```
