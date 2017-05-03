import requests
from bs4 import BeautifulSoup
import re
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
#这个函数获得站内搜索
def seach():
    search_url = 'https://www.lightnovel.cn/search.php?'
    session = requests.session()
    s = session.get(search_url, headers=headers, verify=False)#https协议报错去除
    content = s.text  # 创建一个实例来容纳获取formhash前的搜索界面
    #  使用正则表达式获取搜索formhash
    soup = BeautifulSoup(content,'lxml')
    items = soup.find_all(attrs={"name":"formhash"})
    hash =re.findall('(?<=value=")\w*(?=")',str(items))
    seach_txt = input('请输入搜索：')
    data={
        'hormhash':str(hash),
        'srchtxt':str(seach_txt),
        'searchsubmit':'yes'
    }
    seach_post = session.post(search_url, data=data, headers=headers)
    return seach_post.text
def page_url(txt):
    soup = BeautifulSoup(txt)
    a = soup.find_all(attrs={"class":"pgs cl mbm"})
    if (a == []):
        print('该关键字搜索页只有一页')
    else:
        b = re.findall('(?<=href=").*?(?=")', str(a[0]))
        b.pop()
        return b
def BS_text(text):
    soup = BeautifulSoup(text)
    a = soup.find_all('h3')
    for string in a:
        c = re.findall('(?<=target="_blank">).*?(?=</a>)', str(string))
        b = re.findall('(?<=href=").*?(?=")', str(string))
        d = re.sub('\<.*?\>', '', str(c[0]))
        print(d + '  ' + '网址:https://www.lightnovel.cn/ ' + b[0])
def get_url(url):
    session = requests.session()
    data = session.get(url, headers=headers)
    return data.text



if __name__=='__main__':
    import warnings
    warnings.filterwarnings("ignore")








