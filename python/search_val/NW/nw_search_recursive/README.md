# ion_cli_loop_recursivesearch.py
クライアント側のプログラム。NW上にクエリを流す。

# ion_sample_if_recursive.py
エージェント側のプログラム。出力データのセマンティックをリッスンし、適当なクエリがきたら入力データのセマンティックをクエリとしてNW上に流す。

# time_analysis_svrN_multi_recursive.py
縦軸が再帰的検索にかかった時間、横軸がNW上のエージェント数のグラフを出力する。用いたデータは、result/nw_search_recursive/if10_multi_all.xlsx、result/nw_search_recursive/if_20_multi_all.xlsx、result/nw_search_recursive/if30_multi_all.xlsx、result/nw_search_recursive/if40re2_recursive.xlsx、result/nw_search_recursive/if50_recursive_multi_all.xlsx

出力されるグラフは以下

<img width="325" alt="image" src="https://github.com/nakajimalab-bmi-tmd/ion_2023/assets/103047091/151265a6-21fd-4295-985b-685b9ba69c50">
