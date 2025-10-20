# 使用 requests 工具
import requests
# 使用 json 工具
import json

from smart_blackjack_39_v2 import my_headers

# 使用 GET 方式下載普通網頁
# url = 'https://httpbin.org/get'
# res = requests.get(url)
#
# # 伺服器回應的狀態碼
# # 參考網頁: https://reurl.cc/2DRpan
# # print(res.status_code)
# # print(res.encoding)  # 回傳資料的編碼
# # print(res.text)
# #　get方法的 query string('key': 'value1', 'key2': 'value2)
# my_params={
#     'key1': 'value1',
#     'key2': 'value2'
# }
# # /?key1=value1&?key2=value2
# res1 = requests.get(url, params=my_params)  # 引入query string
# # print(res.url)
# # print(res.text)
# # Post方法:form-data
# my_data = {
#     'key1': 'value1',
#     'key2': 'value2'
# }
# res2 = requests.post(url, data=my_data)
# print(res2.text)
# Web API（Web 應用程式介面）是一個網頁伺服器與應用程式之間的介面，
# 允許網頁程式碼與其他服務或應用程式進行通訊和資料交換。 Web API 利用標準的HTTP 協定進行通訊，並定義了URL、HTTP 方法（如GET、POST）以及資料格式（如JSON）等規格，讓不同軟體之間能夠互相傳遞資訊和請求服務。
# 要上傳的檔案 (變數名稱為 my_filename)
# 自訂標頭 headers(讓人家知道你是真的使用者!)
# my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'}
# res = requests.get(url, headers=my_headers)
# print(res.text)
# 自訂Cookies格式
# my_cookies = {
#     'key1': 'Lebron',
#     'key2': 'James',
#     'key3': 'play',
#     'key4': 'basketball',
#     'key5': 'in',
#     'key6': 'NBA'
# }
from random import randint
from time import sleep

for page in range(1, 4):
 url = f'https://greenliving.moenv.gov.tw/newPublic/APIs/Restaurant4/{page}'
 res = requests.get(url)

# 將 json 轉成物件
 obj = res.json()  # 或使用 obj = res.json()
 print(f'<<<第{page}頁>>>')
 for o in obj['Detail']:
  print('=' * 50)
  print(o['CityName'])
  print(o['Name'])
  print(o['Address'])
  print(o['Phone'])
  print(o['ImgByte'])
 sleep(randint(1, 3))  #暫停間隔






