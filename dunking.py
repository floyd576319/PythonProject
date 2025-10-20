# 匯入套件
from bs4 import BeautifulSoup as bs
import requests as req
from pprint import pprint
import json

# 取得新聞列表
url = "https://www.ptt.cc/bbs/NBA/index.html"

# 用 requests 的 get 方法把網頁抓下來
res = req.get(url)
soup = bs(res.text, 'lxml')
# 建立list來放置列表資訊
list_posts = []
# 清空放置列表資訊的變數 => 避免丟重複的資料
list_posts.clear()
# 取得列表文字&超連結
for a in soup.select('div.r-ent>div.title>a[href]'):
    # print(a.get_text()) # 印出內文
    # print(a['href'])    # 印出超連結元素

    # 加入列表資訊，用dictionary的方式
    list_posts.append({
        'title': a.get_text(),
        'link': 'https://www.ppt.cc' + a['href']
    })
with open('ptt.json', 'w', encoding='utf-8') as file:
    file.write(
        json.dumps(list_posts, ensure_ascii=False, indent=4))
    # indent: 縮排　（縮排過後的資料排列會比較整齊）
    # 但是縮牌所形成的空白也會佔據多餘的儲存空間(流量)
# 走訪每一個超連結的內容
for index, obj in enumerate(list_posts):
    res_ = req.get(obj['link'])
    soup_ = bs(res_.text, 'lxml')
# 你想砍掉超連結頁面內文中的一些內容/資料
# 去掉 div.article-metaline (作者、標題、時間…等)
    for div in soup_.select('div[class^="article-metaline"]'):
        div.decompose()  # decompose函式就可以執行砍掉帶有該屬性的元素
    # 再刪除推文之前，可以先查看推文(div class="push")的數量，以免刪了個寂寞
    if len(soup_.select('div.push')) > 0:
        for div in soup_.select('div.push'):
            div.decompose()
    # 取得實際需要的內容
    html = soup_.select_one('div#main-content').decode_contents() # id=: #
    # 整合到列表資訊的變數當中
    list_posts[index]['html']= html

# pprint(list_posts)
#　取得多個分頁的技巧
# 清空放置列表資訊的變數
list_posts.clear()

# 起始頁數
init_page = 6504

# 最新頁數
latest_page = 6505

# 在已經知道分頁數的情況下
for page in range(init_page, latest_page + 1):

    # 取得新聞列表
    url = f"https://www.ptt.cc/bbs/NBA/index{page}.html"

    # 用 requests 的 get 方法把網頁抓下來
    res = req.get(url)

    # 指定 lxml 作為解析器
    soup = bs(res.text, "lxml")

    # 取得 列表 的文字與超連結
    for a in soup.select('div.r-ent div.title a[href]'):
        # 加入列表資訊
        list_posts.append({
            'title': a.get_text(),
            'link': 'https://www.ptt.cc' + a['href']
        })

# 走訪每一個 a link，整合網頁內文
for index, obj in enumerate(list_posts):
    res_ = req.get(obj['link'])
    soup_ = bs(res_.text, "lxml")

    # 去掉 div.article-metaline (作者、標題、時間…等)
    for div in soup_.select('div[class^="article-metaline"]'):
        div.decompose()

        # 去掉 div.push (推文: 推、→、噓) (判斷去掉元素是否存在)
    if len(soup_.select('div.push')) > 0:
        for div in soup_.select('div.push'):
            div.decompose()

        # 取得實際需要的內容 (類似 JavaScript 的 innerHTML)
    html = soup_.select_one('div#main-content').decode_contents()

    # 整合到列表資訊的變數當中
    list_posts[index]['html'] = html

# 預覽所有結果
pprint(list_posts)















