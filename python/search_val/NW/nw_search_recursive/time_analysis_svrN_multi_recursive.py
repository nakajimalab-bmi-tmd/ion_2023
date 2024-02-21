import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


data_svr10 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/10/if10_re2/if10_multi_all.xlsx")
data_svr20 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/20/if20_re/if_20_multi_all.xlsx")
data_svr30 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/50/re (6)/if30_multi_all.xlsx")
data_svr40 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/40/40re2/if40re2_recursive.xlsx")
data_svr50 = pd.read_excel("/Users/inaokayuu/Desktop/python_research/result/cap/if_recrsive/50/if50_recursive_multi_all.xlsx")
#print(data_svr10.iloc[2:15,12])
svr10_list = data_svr10.iloc[3:33,11].tolist()
svr20_list = data_svr20.iloc[3:33,21].tolist()
svr30_list = data_svr30.iloc[3:33,31].tolist()
svr40_list = data_svr40.iloc[3:33,42].tolist()
svr50_list = data_svr50.iloc[3:33,51].tolist()

svr10_med = np.median(svr10_list)
svr20_med = np.median(svr20_list)
svr30_med = np.median(svr30_list)
svr40_med = np.median(svr40_list)
svr50_med = np.median(svr50_list)
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots()
coefficients = np.polyfit([10,20,30,40,50],[svr10_med,svr20_med,svr30_med,svr40_med,svr50_med], 1)
poly = np.poly1d(coefficients)
#ax.scatter([10,20,30,40,50], [svr10_med,svr20_med,svr30_med,svr40_med,svr50_med],label='Data')
ax.plot( [10,20,30,40,50],poly([10,20,30,40,50]), color='skyblue', linestyle = "dashed",label='Approximate straight line')
plt.legend()
#☟箱ひげ図1つの時との違いは,ここでデータを2個引用するだけ！☟
ax.boxplot((svr10_list, svr20_list, svr30_list, svr40_list, svr50_list), positions = [10,20,30,40,50],widths=5,showfliers=True,showcaps=True)
scale_name = [10, 20, 30, 40, 50]
plt.xticks([10,20,30, 40, 50], scale_name)
plt.xlabel('the number of algorithm',{'fontsize':15}) #文字サイズ
plt.ylabel('Recursive retrieval time [sec]',{'fontsize':15}) #文字サイズ
plt.show()

