# ion_cli_loop_if_val_con.py
クライアント側のプログラム。単位時間あたりのクエリ数を調整して、NW上に設定値までクエリを流し続ける。ion_cli_loop_if_val_rcv.pyと同時に実行する。

# ion_cli_loop_if_val_rcv.py
クライアント側のプログラム。エージェント（サーバ）からの返答を受け取るプログラム。ion_cli_loop_if_val_con.pyと同時に実行する。

# ion_svr_if_send_cnt.py
エージェント側のプログラム。NW上に流れたクエリのセマンティックを認識し、認識できた数をカウントする。カウントした数を標準出力する。

# packet_loss.py
ion_svr_if_send_cnt.pyで標準出力されるカウント数をもとに検索ロス率を計算し、散布図を生成するプログラム。カウント数はプログラムに直に書き込んだ。
縦軸が検索ロス率、横軸が単位時間あたりのクエリ数である。
出力されるグラフは以下

<img width="339" alt="image" src="https://github.com/nakajimalab-bmi-tmd/ion_2023/assets/103047091/5af2db12-1e90-4921-9a9b-9ca693b61fa7">

