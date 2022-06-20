## json to csv

import json
import pandas as pd

for b in range(0,len(dict1[corp1])):
    with open(dict1[corp1][b]+'.json', 'r', encoding = "utf-8") as f:
        a = json.loads(f.read())

        df = pd.json_normalize(a)
        df.to_csv('Dcard_'+dict1[corp1][b]+'.csv', encoding='utf-8-sig', index=False)

for b in range(0,len(dict1[corp2])):
    with open(dict1[corp2][b]+'.json', encoding = "utf-8") as f:
        a = json.loads(f.read())

        df = pd.json_normalize(a)
        df.to_csv('Dcard_'+dict1[corp2][b]+'.csv', encoding='utf-8-sig', index=False)

##合併所有 Dard_ 開頭的csv檔案。存成concatted7_final.csv，不要index，並且以utf-8-sig編碼

from glob import glob
 
files = glob('Dcard_*.csv')
df2 = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
df2.to_csv( 'concatted7_final.csv', index=False, encoding="utf-8-sig" )