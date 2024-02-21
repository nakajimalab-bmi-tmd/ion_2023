# ion_cli_loop_if_val_con.py
クライアント側のプログラム。単位時間あたりのクエリ数を調整して、NW上に設定値までクエリを流し続ける。ion_cli_loop_if_val_rcv.pyと同時に実行する。

# ion_cli_loop_if_val_rcv.py
クライアント側のプログラム。エージェント（サーバ）からの返答を受け取るプログラム。ion_cli_loop_if_val_con.pyと同時に実行する。

# ion_svr_if_send_cnt.py
エージェント側のプログラム。NW上に流れたクエリのセマンティックを認識し、認識できた数をカウントする。カウントした数を標準出力する。

# packet_loss.py
ion_svr_if_send_cnt.pyで標準出力されるカウント数をもとに検索ロス率を計算し、箱ひげ図を生成するプログラム。
