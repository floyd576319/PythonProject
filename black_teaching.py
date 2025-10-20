# 建立一副完整的牌
def create_deck():
    suits= ['♠', '♥', '♦', '♣']
    ranks= ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [rank + suit for suit in suits for rank in ranks]
    return deck
import random

deck = create_deck()
print(deck[:5])  # ['A♠', '2♠', '3♠', '4♠', '5♠']
print(len(deck))  # 52
random.shuffle(deck) #洗牌
card = deck.pop() #抽牌
print(f"你抽到的卡是:{card}")
# 根據 21 點規則進行簡化：
# A → 11 點
# 2~10 → 本身數字
# J, Q, K → 10 點
def card_value(card):
    rank =card[:-1] #去掉最後的花色
    if rank in ['J','Q','K']: #卡牌點數分類判斷式
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)
print(card_value('A♠'))   # 11
print(card_value('10♦'))  # 10
print(card_value('Q♣'))   # 10
print(card_value('5♥'))  # 5

