import numpy as np
# ndarr01 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# print(ndarr01)
# print(ndarr01.shape)
# # 多維陣列的形狀shape, 維度 = 資料的層次
# ndarr02 = np.array([[1, 2, 3, 4],[5, 6, 7, 8]])
# print(ndarr02)
# print(ndarr02.shape) #(層次, 每層資料數量)
# print(ndarr02.T.shape)# 資料的轉置(transpose)
# print(ndarr02.ravel()) # 扁平化資料
# print(ndarr02.shape)
# ndarr03 = np.array([[[1, 2], [3, 4], [5, 6],[7, 8]]])
# print(ndarr03)
# ndarr03 = np.array([[[2, 3], [5, 4]], [[2, 0], [5, 7]]])
# print(ndarr03)
# print(ndarr03.shape)
# 扁平化資料 => 降維技巧(多維 => 一維)
# 重塑資料形狀 => 改變資料形狀，但資料數量保持不變
# ndarr04 = np.array([[[2, 4], [5, 1]], [[7, 10], [3, 0]]])
# print(ndarr04)
# print(ndarr04.shape)
# print(ndarr04.size)
# print(ndarr04.reshape(4, 2))
# data01 = np.zeros(14)
# print(data01)
# data02 = np.empty(20).reshape(2, 2, 5)
# print(data02)
# print(data02.shape)
data03 = np.array([[2, 4], [11, 5]])
print(data03)
print(data03.ravel())
print(data03.shape)
print(data03.T.shape)















