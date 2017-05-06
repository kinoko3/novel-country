from bs4 import BeautifulSoup
import requests, re, threading, time, sqlite3
import warnings,traceback
warnings.filterwarnings("ignore")
session = requests.session()
conn = sqlite3.connect('download_tittle.db')
cursor = conn.cursor()
cursor.execute('''create table title
(ID int PRIMARY KEY NOT NULL, NAME varchar(2000) NOT NULL, URL varchar(2000) NOT NULL );''')
def url_for():
    s = session.get(url, headers=headers, verify=False, cookies=cookies)
    content = s.text
    soup = BeautifulSoup(content, 'lxml')
    s1 = soup.find_all("a", class_="last")
    b = re.findall('(?<=>...).*?(?=</a>)', str(s1[0]))
    url_content = []
    for url_x in range(1, int(b[0])+1):
        s = re.sub('(?<=forum-56-).*?(?=.html)', str(url_x), 'https://www.lightnovel.cn/forum-56-.html')
        url_content.append(s)
    return url_content
url = 'https://www.lightnovel.cn/forum-56-1.html'#re模块里面的sub()和subn()替换

cookies = {'UM_distinctid': '15b3b46b9c30-007caf321d85dc-396a7807-1fa400-15b3b46b9c414fe', 'lightnovel_0a3d_lastcheckfeed': '483351%7C1491731230', 'lightnovel_0a3d_nofavfid': '1', 'lightnovel_0a3d_saltkey': 'w5x3NxN6', 'lightnovel_0a3d_lastvisit': '1494030152', 'lightnovel_0a3d_sendmail': '1', 'lightnovel_0a3d_visitedfid': '56D173D91D4', 'lightnovel_0a3d_viewid': 'tid_886373', 'lightnovel_0a3d_secqaaS0': 'd5cfEa%2B0Ge46QDDEKiWP9bCl67GAylkH3xD%2FT5CCSTs%2BVE54o8cEwS%2FWtMiJvPwfNZxeY8hf1HXAt%2Fl1yk%2Fy5QXIXez9hyFholmi%2FRlex8CbA6nH', 'lightnovel_0a3d_seccodeS0': 'c37199IQ2LNllp3YdtU7LWQJLPBI0F30Ee%2BQXANIsOqsqr%2BT1IbBYBKLqzWNgGGFrWvikPVbPOk', 'lightnovel_0a3d_con_request_uri': 'http%3A%2F%2Fwww.lightnovel.cn%2Fconnect.php%3Fmod%3Dlogin%26op%3Dcallback%26referer%3Dforum.php%253Fmod%253Dforumdisplay%2526fid%253D56%2526page%253D3', 'lightnovel_0a3d_client_created': '1494033948', 'lightnovel_0a3d_client_token': '255EB46BF782F3D2B9AC22B1ED428E8C', 'lightnovel_0a3d_ulastactivity': '1494033948%7C0', 'lightnovel_0a3d_auth': 'a1eep%2BFFUFx4uW4s0RX65OM9%2BswJRT8h6R%2FrBVhCWsZ1G%2B2dbRL%2F3aUpJGIFjcQnXHA8pc5gd%2B5czqXeRDGbnRGBifE', 'lightnovel_0a3d_connect_login': '1', 'lightnovel_0a3d_connect_uin': '255EB46BF782F3D2B9AC22B1ED428E8C', 'lightnovel_0a3d_checkpm': '1', 'lightnovel_0a3d_forum_lastvisit': 'D_173_1493940116D_56_1494033952', 'CNZZDATA3599420': 'cnzz_eid%3D620048360-1491345381-%26ntime%3D1494030343', 'lightnovel_0a3d_noticeTitle': '1', 'lightnovel_0a3d_lastact': '1494033954%09connect.php%09check', 'lightnovel_0a3d_connect_is_bind': '1', 'lightnovel_0a3d_smile': '5D1'}
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
                #写一个错误捕捉并输出错误到log文件
                try:
                    cursor.execute('''INSERT OR IGNORE INTO title (ID, NAME, URL) VALUES ('%d','%s','%s')''' %(_id, c[0], b[0]))
                except :
                    f = open(r'error_log.txt', 'a+', errors='ignore')
                    traceback.print_exc(file=f)
                    f.flush()
                    f.close()
if __name__ == '__main__':
    lst_url = url_for()
    t = threading.Thread(target=main(lst_url))
    t.start()
    t.join()
    cursor.close()
    conn.commit()
    conn.close()








