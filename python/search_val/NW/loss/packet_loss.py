import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


data_svr10 = pd.read_excel("/Users/inaokayuu/Desktop/if_recursive_multi/if10recursive_multi_sumtime.xlsx")
data_svr20 = pd.read_excel("/Users/inaokayuu/Desktop/if_recursive_multi/if20_recursive_multi_sumtime.xlsx")
data_svr30 = pd.read_excel("/Users/inaokayuu/Desktop/if_recursive_multi/if30_recursive_multi_sumtime.xlsx")


time_1000 = 1000-(958+954+958+958+957+960+953+963+944+942)/10
time_2000 = 1000-(731+786+705+803+755+786+804+752+766+812)/10
time_2500 = 1000-(568+605+626+734+721+703+643+696+732+632)/10
time_3000 = 1000-(547+637+640+524+604+665+645+647+534+522)/10
time_5000 = 1000-(550+533+506+593+600+544+641+576+489+539)/10
time_8000 = 1000-(465+591+476+617+556+466+447+516+526+483)/10
time_10000 = 1000-(444+414+524+478+473+552+547+521+554+426)/10
#print(data_svr20.iloc[0:15,1])
#time_01 = (1000-997)/1000
plt.rcParams['font.family'] = 'Times New Roman'

y = [ time_1000/1000, time_2000/1000, time_2500/1000, time_3000/1000,time_5000/1000,time_8000/1000,time_10000/1000]
x = [1000, 2000,2500,3000, 5000,8000,10000]
plt.scatter(x, y)
plt.xlabel('Query [times/sec]',{'fontsize':15}) #文字サイズ
plt.ylabel('Ratio of loss',{'fontsize':15}) #文字サイズ
plt.show()

