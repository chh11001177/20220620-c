#pip install -U fake_useragent
from requests import session
import time
import random
import json
from fake_useragent import UserAgent
from lxml import html

def search_article(corp = '饗賓集團', brand = '饗饗'):
    
    ua = UserAgent(use_cache_server=False)
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    s = session()
    
    api = 'https://www.dcard.tw/service/api/v2'
    url = api + '/search?forum=food&query='+ brand

    res = s.get(url, headers = headers)
    html = res.text
    rejs = json.loads(html)

    final_art = []
    #存取文章
    for i in rejs:
        a = {}
        a['Corp'] = corp
        a['Brand'] = brand
        a['Platform'] = "Dcard"
        a['Branch'] = ""
        a['Username'] = i['memberId']
        a['ReviewTime'] = i['createdAt'][0:10]
        a['Title'] = i['title']
        a['ReviewContent'] = i['excerpt']
        a['ReviewStar'] = ""
        a['commentCount'] = i['commentCount']
        final_art.append(a)
        
        #爬回文資訊
        url2 = api+ '/posts/'+ str(i['id']) + '/comments'
        res2 = s.get(url2, headers = headers)
        html2 = res2.text
        CmntsData = json.loads(html2)
        
        comment_content = []
        print('正在爬這篇文章', i['title'])
        time.sleep(random.randint(1,5))
        for j in CmntsData:
            try:
                b = {}
                b['Corp'] = corp
                b['Brand'] = brand
                b['Platform'] = "Dcard"
                b['Branch'] = ""
                b['Username'] = j['id']
                b['ReviewTime'] = j['createdAt'][0:10]
                b['Title'] = i['title']
                b['ReviewContent'] = j['content']
                b['ReviewStar'] = ""
                b['commentCount'] = ""
                comment_content.append(b)
                print('正爬到第', j['floor'], '樓')
                time.sleep(random.randint(1,3))
            except KeyError:
                print('留言被刪除')
                continue
   
        for i in comment_content:
            final_art.append(i)
            
    return final_art


def output(filename, data):
    try:
        with open(filename +".json", 'wb+') as f:
            f.write(json.dumps(data, indent=1, ensure_ascii=False).encode('utf-8'))
            print('爬取完成', filename + '.json', '輸出成功')
    except Exception as err:
        print(filename +'.json', '輸出失敗')
        print('error message:', err)

#建立字典與陣列以便做迴圈

dict1= {'饗賓集團':['饗饗','旭集','饗泰多','饗食天堂','果然匯','小福利火鍋','開飯川食堂','真珠'],
        '王品集團':['12mini','丰禾','王品','石二鍋','肉次方','西提','尬鍋','享鴨','和牛涮','青花驕','品田牧場','原燒','夏慕尼','莆田','陶板屋','最肉燒肉','聚北海道鍋物','藝奇','hot7','the wang']}
corp1 = '饗賓集團'
corp2 = '王品集團'

#饗賓迴圈執行完 接著執行王品迴圈
for a in range(0,len(dict1[corp1])):
    data = search_article(corp = corp1, brand = dict1[corp1][a])
    output(dict1[corp1][a], data)

for a in range(0,len(dict1[corp2])):
    data = search_article(corp = corp2, brand = dict1[corp2][a])
    output(dict1[corp2][a], data)