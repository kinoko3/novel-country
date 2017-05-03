import re, requests, sqlite3, threading
conn = sqlite3.connect('tittle.db')
cursor = conn.cursor()
values = cursor.execute('''select * from title''')
url = 'https://www.lightnovel.cn/'
title = input("输入书名：")
def main():
    for row in values:
        m = re.search(title, row[1])
        if m:
            print(row[1]+'\n')
            print(url+row[2])
    print('搜索完成')
t = threading.Thread(target=main())
t.start()
t.join()