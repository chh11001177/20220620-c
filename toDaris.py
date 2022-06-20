from pymysql import escape_string #PyMySQL==0.9.3
import mysql.connector #python -m pip install mysql-connector
import json

#我們是用MAMP做 之後再轉到AWS
def creat_database(dbname):
    mydb = mysql.connector.connect(
        host="localhost",
        port=8889,
        user="root",
        password="root"
      )
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbname))
    mydb.close()

#name =>tablename place => 看是哪裡爬蟲的 我們是有分開變成json檔案 去掉place也行
def insertMessage(name,place,dbname):
    mydb = mysql.connector.connect(
        host="",
        port=3306,
        user="",
        password="",
        database=dbname,
        charset='utf8mb4'
      )
    cursor = mydb.cursor()
    # 建立table
    creat_tabel = """
        CREATE TABLE IF NOT EXISTS `{}`
    #注意 !!! 這裡要改成你的col name
        !!!=>>>>>(id INT AUTO_INCREMENT PRIMARY Key,date  DATE,content VARCHAR(10000))<<<<要更改
        """.format(name)
    cursor.execute(creat_tabel)
    #要存入emoji
    sql = f'''
    ALTER TABLE `{name}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    '''
    cursor.execute(sql)
    data = json.load(open(name + '_' + place + '.json','r',encoding='utf-8'))
    for row in data:
        # content =>要改成你們要的col time=>也是 改成你們的col  .split('T') =>要看你們時間格式有沒有T 沒有就可以刪除
        sql = f'''INSERT INTO `{name}` (date,content) VALUES (%s, %s)'''
        val = (row['time'].split('T')[0], escape_string(row['content']))
        cursor.execute(sql, val)
    mydb.commit()
    mydb.close()

if __name__ == "__main__":
    dbname = ""
    creat_database(dbname)
    #輸入你們的品牌 place如果上面有刪除下面就不需要
    names = ['王品','夏慕尼','西堤','石二鍋','非常泰','瓦城','時時香','1010湘']
    places = 'ig'
    for name in names:
        insertMessage(name,places)