import numpy as np
# a= np.array([[5,6],[7,8]])
# b= np.array([[1,2],[3,4]])
# print(a.shape)
# print(b.shape)
# print(a.ndim)
# print(b.ndim)#維度:1
# print(a.dtype) #資料型別: int64
# print(a[0,0])
# print(b[0,1])
# print(a // b)
# print(a>b)
# print(a[a>6])
# x =np.array([[1,2],[3,4]])
# print(x)
# print(x.T)
# y= np.array([[6,7],[8,9]])
# print(np.concatenate((x,y))) #陣列合併
# print(np.stack((x,y), axis=2))
# print(np.stack((x,y), axis=0))
# print(y.T)
#陣列的統計方法
# x =np.array([1,2,3,4,5])
# y= np.array([6,7,8,9,10])
# print(np.concatenate((x,y)))
# print(np.stack((x,y),axis=0))
# print(x>2)
# print(np.mean(x))
# print(np.std(x)) #標準差
# print(np.min(x)) #最小值
# print(np.max(x)) #最大值
# np.random.seed(0) #設定亂樹種子
# r= np.random.randint(0,10,6)
# print(r)
# print(x.ndim)
# print(x.shape)
# print(x.dtype)
r =np.random.randint(50,101,20)
print(r)
print(np.mean(r))
print(np.std(r))
print(np.min(r))
print(np.max(r))
avg= np.mean(r)
above_mean= r[r>avg]
x= np.array([1,2,3])
print(x[x>2])
print(f"高於平均的有:{above_mean}")

