import folium

# 地圖中心位置（例如：台北101）
latitude = 24.130702356199404
longitude = 120.64266401088567

# 建立地圖物件
map_object = folium.Map(location=[latitude, longitude], zoom_start=15)

# 加上地標（Marker）
folium.Marker(
    [latitude, longitude],
    popup="豐樂公園",
    tooltip="點我看資訊"
).add_to(map_object)

# 另外加一個地點（例如台北車站）
folium.Marker(
    [24.12998547975323, 120.64567936525484],
    popup="台中秀泰文心影城",
    icon=folium.Icon(color="green")
).add_to(map_object)

# 匯出成 HTML 檔案，並用瀏覽器打開
map_object.save("map.html")
print("✅ 地圖已儲存為 map.html，用瀏覽器開啟觀看！")
