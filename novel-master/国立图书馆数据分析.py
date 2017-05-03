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

cookies = {'lightnovel_0a3d_saltkey': 'skxm9XrD',
           'lightnovel_0a3d_lastvisit': '1491344538',
           'UM_distinctid': '15b3b46b9c30-007caf321d85dc-396a7807-1fa400-15b3b46b9c414fe',
           'lightnovel_0a3d_sendmail': '1',
           'lightnovel_0a3d_seccodeS0': '7403%2BRLo%2BF4LKalinaBR5GqSBpamtw87Hozz8j0QFtplOt7iorjRT89uKI8S5QUDy3fl4Xq%2FXoY',
           'lightnovel_0a3d_ulastactivity': '1491731230%7C0',
           'lightnovel_0a3d_auth': 'ad4a1QrRuE2E8Hrwtb3TSyE7Q90HXeImss0qFXQSAl%2BqlLY6WGKtCtQQbouHmdCyl%2F7hgiJPtpowQC%2FjnkkdHNn8dzQ',
           'lightnovel_0a3d_lastcheckfeed': '483351%7C1491731230',
           'lightnovel_0a3d_checkfollow': '1',
           'lightnovel_0a3d_nofavfid': '1',
           'lightnovel_0a3d_onlineusernum': '3461',
           'CNZZDATA3599420': 'cnzz_eid%3D620048360-1491345381-%26ntime%3D1491727663',#不变
           'lightnovel_0a3d_checkpm': '1', 'lightnovel_0a3d_noticeTitle': '1',
           'lightnovel_0a3d_lastact': '1491731235%09connect.php%09check',
           'lightnovel_0a3d_connect_is_bind': '1',
           'lightnovel_0a3d_ignore_notice': '1'}
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








