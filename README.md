# vrrc
VRラジコン用

# SSH情報
ssh pi@172.16.2.159  
pw: raspberry  

# ラズパイ側パス
cd /home/pi/vrrc  

# server起動
sudo ~/local/python-3.5.2/bin/python main/server.py  
※sudoしないとwiringpiが使えないで  

# ライブラリinstallについて
1. requirements.txtにライブラリ名==バージョン の行を足す
2. pip install -r requirements.txt

# websocket
URI: ws://172.16.2.159:9090/ws

Chromeのwebsocketお試しplugin を使うとテストしやすい
https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo

# websocket message format
JSON。command&valueの配列を垂れ流しで送信  
steering: -1.0〜1.0  
acceleration: -1.0〜1.0  

内部的にはそれぞれ
steering: 40〜122  
acceleration: 60(reverse)〜70(neutral)〜80(forward)  
でGPIOにPWM出力してます  

例：
```
[
  {
    "command": "steering",
    "value": -0.7677
  },
  {
    "command": "acceleration",
    "value": 0.6032
  },
  {
    "command": "steering",
    "value": -0.6998
  },
  ...
]
```
