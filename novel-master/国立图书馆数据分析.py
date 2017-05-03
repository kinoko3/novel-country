from bs4 import BeautifulSoup
import requests, re, threading, time, sqlite3
import warnings
warnings.filterwarnings("ignore")
session = requests.session()
conn = sqlite3.connect('tittle.db')
cursor = conn.cursor()
cursor.execute('''create table title
(ID int PRIMARY KEY NOT NULL, NAME varchar(2000) NOT NULL, URL varchar(2000) NOT NULL );''')
def url_for():
    url_content=[]
    for url_x in range(1, 71):
        s = re.sub('(?<=forum-91-).*?(?=.html)', str(url_x), 'https://www.lightnovel.cn/forum-91-.html')
        url_content.append(s)
    return url_content
#url = 'https://www.lightnovel.cn/forum-91-1.html'#re模块里面的sub()和subn()替换

cookies = {}
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }


def main(lst_url):
    _id = 0
    for url in lst_url:
        s = session.get(url, headers=headers, verify=False, cookies=cookies)
        content = s.text
        soup = BeautifulSoup(content, 'lxml')
        s1 = soup.find_all("a", class_="s xst")
        cout = 0
        for _str in s1:
            cout = cout + 1
            if cout < 10:
                pass
            else:
                _id = _id + 1
                c = re.findall('(?<=">).*?(?=</a>)', str(_str))
                b = re.findall('(?<=href=").*?(?=")', str(_str))
                print(c[0])
                print(b[0])
                cursor.execute('''INSERT OR IGNORE INTO title (ID, NAME, URL) VALUES ('%d','%s','%s')''' %(_id, c[0], b[0]))
if __name__ == '__main__':
    lst_url = url_for()
    t = threading.Thread(target=main(lst_url))
    t.start()
    t.join()
    cursor.close()
    conn.commit()
    conn.close()








