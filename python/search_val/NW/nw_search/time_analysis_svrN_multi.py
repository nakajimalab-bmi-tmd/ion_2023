import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


data_svr10 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/10/if10_re2/if10_multi_all.xlsx")
data_svr20 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/20/if20_re/if_20_multi_all.xlsx")
data_svr30 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/50/re (6)/if30_multi_all.xlsx")
data_svr40 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/40/40re2/if40re2_recursive.xlsx")
data_svr50 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/50/if50_recursive_multi_all.xlsx")
#print(data_svr10.iloc[2:15,12])
svr10_list = data_svr10.iloc[3:33,3].tolist()
svr20_list = data_svr20.iloc[3:33,3].tolist()
svr30_list = data_svr30.iloc[3:33,3].tolist()
svr40_list = data_svr40.iloc[3:33,4].tolist()
svr50_list = data_svr50.iloc[3:33,3].tolist()

plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots()

#ax.scatter([10,20,30,40,50], [svr10_med,svr20_med,svr30_med,svr40_med,svr50_med],label='Data')
#☟箱ひげ図1つの時との違いは,ここでデータを2個引用するだけ！☟
ax.boxplot((svr10_list, svr20_list, svr30_list, svr40_list, svr50_list), showfliers=True,showcaps=True)
scale_name = [10, 20, 30, 40, 50]
plt.xticks([1,2,3, 4, 5], scale_name)
plt.xlabel('the number of algorithm',{'fontsize':15}) #文字サイズ
plt.ylabel('Retrieval time [sec]',{'fontsize':15}) #文字サイズ
plt.show()

