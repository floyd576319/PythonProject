import requests as req
from bs4 import BeautifulSoup as bs

 # PTT Gossiiping (八卦版)
url = "https://www.ptt.cc/bbs/Gossiping/index.html"

# 首頁網址
prefix = 'https://www.ptt.cc'

#設定cookie
my_cookies = {
    'over18': '1'
}
#請求
res = req.get(url, cookies = my_cookies)
#取得soup物件
soup = bs(res.text, 'lxml')
#顯示列表
for a in soup.select('div.r-ent > div.title > a'):
    print(a.get_text())  #文章內容
    print(prefix + a['href'])  #文章網址
