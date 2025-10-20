import random
low=1
high=1000
number=random.randint(low,high)
guesses=0
while True:
    guess=int(input(f'請猜一個介於{low}~{high}之間的數字:'))
    guesses+=1
    if guess<number:
        print('猜的數字太小了')
    elif guess>number:
        print('猜的數字太大了')
    else:
        print('恭喜你猜對了!這個數字就是{number}')
        print(f'你總共猜了{guesses}次。')
        break













