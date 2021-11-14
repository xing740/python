import requests
import pandas as pd
import csv
#url = "https://www.mataf.net/en"
url = "https://www.mataf.io/api/tools/csv/correl/snapshot/forex/50/correlation.csv?symbol=AUDCAD|AUDCHF|AUDJPY|AUDNZD|AUDUSD|CADCHF|CADJPY|CHFJPY|EURAUD|EURCAD|EURCHF|EURGBP|EURJPY|EURNZD|EURUSD|GBPAUD|GBPCAD|GBPCHF|GBPJPY|GBPNZD|GBPUSD|NZDCAD|NZDCHF|NZDJPY|NZDUSD|USDCAD|USDCHF|USDJPY"
r = requests.get(url)
#print(r.text)



s_arr = r.text.split('\n')
f_arr = []
for i in range(len(s_arr)): 
	if i <= 3:continue
	tmpArr = s_arr[i].split(',')
	f_arr.append(tmpArr[0: 3])

_data = pd.DataFrame(f_arr)
_data.to_csv('correlation.csv', index = False, encoding = 'utf-8')