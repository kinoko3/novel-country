import re
def url_for():
    url_content=[]
    for url_x in range(1, 71):
        s = re.sub('(?<=forum-91-).*?(?=.html)', str(url_x), 'https://www.lightnovel.cn/forum-91-.html')
        url_content.append(s)
    return url_content









