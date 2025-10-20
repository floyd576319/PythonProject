# 收集資料=>清理資料=>分析資料=>基於資料的應用
# pandas實戰
import pandas as pd
# 讀取資料
df = pd.read_csv(r"C:\Users\james\PycharmProjects\pythonProject\.venv\Lib\site-packages\pandas\io\googleplaystore.csv")
# 觀察資料
# print(df)
# print("資料欄位:",df.columns)
# 分析資料:評分的各種統計數據
# 理論上應用程式的評分最高上限是五分(五顆星)
# 篩選是資料清理的其中一個技巧
# condition = df['Rating']<=5  # 正常評分範圍
# df = df[condition]
# print(df[condition])
# print(df['Rating'])
# print("平均數:",df['Rating'].mean())
# print("最小值:",df['Rating'].min())
# print("最大值:",df['Rating'].max())
# print("加總:",df['Rating'].sum())
# print("前一百個應用程式的評分總和:",df['Rating'].nlargest(100).sum())
# print("前一百個評分的平均數:",df['Rating'].nlargest(100).mean())
# print("前一千個評分的平均數:",df['Rating'].nlargest(1000).mean())
# print(df['Rating'].nlargest(10000).mean())
# 分析資料:安裝數量的各種統計數據
# 注意!字串沒辦法進行像是數字的統計運算
# 資料型態的轉換方式
print(df['Installs'].str.contains("Free"))
df['Installs'] = (df['Installs'].str.replace('[+,]','', regex=True).replace('Free','0').astype(int))
print(df['Installs'])
print(df['Installs'].mean())
condition = df['Installs']>100000 # 安裝數量大於十萬次的篩選
print(df['Installs'][condition].shape[0])
# 電腦無法把標點符號識別為數字，因此需要另做(取代)處理

# 基於資料的應用:關鍵字搜尋應用程式名稱
keyword = input("請輸入關鍵字:")
# 搜尋其實就是一種資料的篩選
condition1 = df['App'].str.contains(keyword, case=False)# str contains功能預設結果為小寫，case=False(忽略結果大小寫)
condition2 = df['App'].str.contains(keyword)
# 應用程式的名稱是否包含使用者輸入的關鍵字
print(df['App'][condition1].shape[0])
print(df['App'][condition2].shape[0])









