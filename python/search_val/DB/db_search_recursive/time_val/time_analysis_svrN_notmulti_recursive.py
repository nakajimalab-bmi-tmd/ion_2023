import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


data_svr10 = pd.read_excel("/Users/inaokayuu/Desktop/引き継ぎ/result/db_search_recursive/if10_recursive.xlsx")
data_svr20 = pd.read_excel("/Users/inaokayuu/Desktop/引き継ぎ/result/db_search_recursive/if20_recursive.xlsx")
data_svr30 = pd.read_excel("/Users/inaokayuu/Desktop/引き継ぎ/result/db_search_recursive/if30_recurisve.xlsx")
data_svr40 = pd.read_excel("/Users/inaokayuu/Desktop/引き継ぎ/result/db_search_recursive/if40_recursive.xlsx")
data_svr50 = pd.read_excel("/Users/inaokayuu/Desktop/引き継ぎ/result/db_search_recursive/if50_recursive_notmuilti.xlsx")
print(data_svr10.iloc[2:15,12])
svr10_list = data_svr10.iloc[1:31,12].tolist()
svr20_list = data_svr20.iloc[1:31,22].tolist()
svr30_list = data_svr30.iloc[1:31,32].tolist()
svr40_list = data_svr40.iloc[1:31,42].tolist()
svr50_list = data_svr50.iloc[1:31,52].tolist()

svr10_med = np.median(svr10_list)
svr20_med = np.median(svr20_list)
svr30_med = np.median(svr30_list)
svr40_med = np.median(svr40_list)
svr50_med = np.median(svr50_list)
plt.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots()

coefficients = np.polyfit([10,20,30,40,50],[svr10_med,svr20_med,svr30_med,svr40_med,svr50_med], 2)
poly = np.poly1d(coefficients)
#ax.scatter([10,20,30,40,50], [svr10_med,svr20_med,svr30_med,svr40_med,svr50_med],label='Data')
ax.plot( [10,20,30,40,50],poly([10,20,30,40,50]), color='skyblue', linestyle = "dashed",label='Approximate curve')
plt.legend()
#☟箱ひげ図1つの時との違いは,ここでデータを2個引用するだけ！☟
ax.boxplot((svr10_list, svr20_list, svr30_list, svr40_list, svr50_list), positions = [10,20,30,40,50],widths=5,showfliers=True,showcaps=True)
scale_name = [10, 20, 30, 40, 50]
plt.xticks([10,20,30, 40, 50], scale_name)
plt.xlabel('the number of algorithm',{'fontsize':15}) #文字サイズ
plt.ylabel('Recursive retrieval time [sec]',{'fontsize':15}) #文字サイズ
plt.show()

