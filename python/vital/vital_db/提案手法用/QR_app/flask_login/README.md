# app.py
Webサーバを起動するプログラム。今回は、HTTPSで実装されているため、SSL証明書がある他の同一LAN内のデバイス（ipadなど）であればこのウェブアプリを利用できる。他のデバイスからアクセする際は、Webサーバを立ち上げているデバイスのIPおよびポート番号をブラウザに入力すれば良い。
<img width="249" alt="image" src="https://github.com/nakajimalab-bmi-tmd/ion_2023/assets/103047091/bd837a1d-ee97-4a55-b5b9-7600745300ef">

実行コマンド
python app.py

# templates
app.pyから呼び出されるhtmlファイルなどがある。

# cert.pem, key.pem
HTTPSでウェブアプリを使用するために必要。HTTPSをやるには、SSL証明書を発行する必要がある。今回はテスト環境のため、簡単にOpenSSLで発行。これは、セキュリティ上いまいちでクライアントからウェブでアクセスすると警告が出る。
うまくやるには、iPad側でMac側で発行した証明書をインストールする必要がある。
証明書のインストールの仕方は以下のサイト
https://support.apple.com/ja-jp/102390
