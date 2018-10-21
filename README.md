# 3DSimulatorWebApp

バックエンドでPython/C++で物理シミュレーションを行い、WebAPI(Python)経由でフロントエンドへ結果を送り、
フロントエンド側ではJavaScriptで3D可視化(threejs)・グラフ化等を行いたいWebアプリ。

(やる気が続けば)下記辺りを対応し色々なシミュレーションモジュールを作りたい予定。

- バックエンド
    - 各種物理シミュレータ(Python/C++)
    - WebAPI(Python  flask/django)
    - 分散/並列処理対応
    - クラウド計算対応

- フロントエンド
    - パラメータ入力/シミュレーション実行・停止等のインターフェース(dat.gui.js?)
    - バックエンドから受け取った計算結果の3D可視化(threejs)
    - 3Dオブジェクトのインタラクティブ操作(クリック&ドラッグで移動等)
    - グラフ機能(C3.js/chart.js?)

## 実行方法

1. 計算サーバー起動

```
$ cd backend
$ python server.py
```

2. 3Dビューアの起動

frontend/index.htmlをブラウザで開く
