from bs4 import BeautifulSoup as bs
import requests as req
from pprint import pprint
import json,re  # re=regex(正規表達式)
# 攻略新聞列表: 圖片 超連結 html
# 刑法有對網路爬蟲的管制及懲處
# 無故以電腦程式或其他電磁方式干擾他人電腦或其相關設備，致生損害於公眾或他人者，處三年以下有期徒刑、拘役或科或併科三十萬元以下罰金。
url = "https://www.healthnews.com.tw/channel/13c2fa31-c4b5-8e0a-a448-96ec7aa8c809/"
res = req.get(url, timeout=10)
soup = bs(res.text, 'lxml')
print(soup)
li_data = []
# 新增前綴網址
prefix = 'https://www.healthnews.com.tw/'
# class=:. id=:#
# src: 圖片的超連結
for li in soup.select('li.media.mb-5.list-item'):
    img = li.select_one('img.mr-1.w-40')
    imgSrc = img['src']
    div = li.select_one('div.media-body.ml-3')
    a = div.select_one('a[href]')
    aTitle = re.sub(r'\s|\r|\n','',a.get_text())  # a的標題
    aLink = a['href']  # a的超連結
    content = div.select_one('div.list-content').get_text()
    # 新增迴圈中預先挑選出的內容(obj)到列表中
    li_data.append({
        'title': aTitle,
        'link': prefix + aLink, # 內文的超連結
        'content': content,
        'img_src': imgSrc       # 圖片的超連結
})
# 建立&開啟檔案
with open ("healthnews.json","w",encoding="utf-8") as file:
    file.write(json.dumps(li_data, ensure_ascii=False, indent=4))


    





