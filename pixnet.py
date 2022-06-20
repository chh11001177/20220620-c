import json
import time
import urllib.parse
from urllib import request
import ssl

#Python requests 移除SSL認證，mac 會報錯所以需要
ssl._create_default_https_context = ssl._create_unverified_context 


corp = '王品集團'
brand = 'THE WANG'   
api = 'https://www.pixnet.net/mainpage/api/'
result = []
for n in range(1,18):  # urllib.parse.quote(brand) >> urlencode brand
    url = api + 'tags/'+ urllib.parse.quote(brand) +'/feeds?page='+  str(n) +'&per_page=5&filter=articles&sort=latest&refer=https%3A%2F%2Fwww.pixnet.net%2Ftags%2F%25E9%25A5%2597%25E9%25A5%2597'
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    headers = {'User-Agent' : UserAgent}
    req = request.Request(url = url , headers = headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    rejs = json.loads(html)


    for i in rejs['data']['feeds']:
      a = {}
      a["Corp"] = corp
      a["Brand"] = brand
      a["Platform"] = "Pixnet"
      a["Branch"] = ""
      a["Username"] = i["display_name"]
      a["ReviewTime"] = time.strftime("%Y-%m-%d", time.localtime(i["created_at"]))
      a["Title"] = i["title"]
      a["ReviewContent"] = i["description"]
      a["ReviewStar"] = ""
      a["commentCount"] = i["reply_count"]
      
      result.append(a)
# time_stamp = i["created_at"] # 設定timeStamp
# struct_time = time.localtime(i["created_at"]) # 轉成時間元組
# timeString = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i["created_at"])) # 轉成字串
# print(timeString)

print(result)
y = json.dumps(result, ensure_ascii = False, indent = 1)
with open(brand+'Pixnet.json', 'w', encoding = "utf-8") as f:
    f.write(y)

