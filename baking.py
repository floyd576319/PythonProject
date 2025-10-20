# Cookies的作用
import requests as req
from bs4 import BeautifulSoup as bs

from mashroom.mashroom import my_cookies

# PTT Gossiiping (八卦版)
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
# 首頁網址
prefix = 'https://www.ptt.cc' # 記得要加前綴網址
# 設定cookies
my_cookies = {'over18': '1'}
# 使用requests get方法把網頁抓下來
res = req.get(url, cookies=my_cookies)
# 指定lxml為解析器
soup = bs(res.text, 'lxml')
print(res.text)
# .: class=
# 顯示連結列表
for a in soup.select('div.r-ent > div.title > a[href]'):
    print(a.get_text())
    print(prefix+a['href']) #完整的網址

