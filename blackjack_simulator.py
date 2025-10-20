import random

# 建立撲克牌
suits = ['♠', '♥', '♦', '♣']
ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
full_deck = [rank + suit for suit in suits for rank in ranks]

# 計算卡牌點數
def card_value(card):
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

# 計算總點數 + A 調整 + 23 點歸零規則
def calculate_score(hand):
    score = sum(card_value(card) for card in hand)
    ace_count = sum(1 for card in hand if card.startswith('A'))
    while score > 39 and ace_count > 0:
        score -= 10
        ace_count -= 1

    if score == 23:
        print("⚠️ 觸發特殊規則：剛好 23 點，點數歸零！")
        score = 0

    return score

# 顯示手牌
def show_hand(hand, owner="玩家"):
    print(f"{owner} 的手牌: {' '.join(hand)}，總點數: {calculate_score(hand)}")

# 智慧莊家補牌策略
def smart_dealer_play(dealer_hand, player_score, deck):
    while True:
        dealer_score = calculate_score(dealer_hand)
        if dealer_score < 30:
            dealer_hand.append(deck.pop())
        elif 30 <= dealer_score <= 33:
            if dealer_score < player_score:
                dealer_hand.append(deck.pop())
            else:
                break
        elif 34 <= dealer_score <= 36:
            if dealer_score <= player_score:
                dealer_hand.append(deck.pop())
            else:
                break
        else:
            break
    return dealer_hand

# 單局對戰邏輯（支援自動與手動）
def play_one_round(auto_play=False):
    deck = full_deck.copy()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # 玩家回合
    while True:
        show_hand(player_hand, "玩家")
        if calculate_score(player_hand) > 39:
            print("玩家爆牌！你輸了這一局。\n")
            return "lose", player_hand, dealer_hand

        if auto_play:
            if calculate_score(player_hand) < 30:
                choice = 'h'
            else:
                choice = random.choice(['h', 's'])
            print(f"🤖 玩家選擇: {choice}")
        else:
            choice = input("要牌 (h) 或 停牌 (s)? ").lower()

        if choice == 'h':
            player_hand.append(deck.pop())
        elif choice == 's':
            break

    # 莊家回合
    dealer_hand = smart_dealer_play(dealer_hand, calculate_score(player_hand), deck)
    show_hand(dealer_hand, "莊家")

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # 勝負判斷
    if dealer_score > 39:
        print("莊家爆牌！你贏了這一局！\n")
        return "win", player_hand, dealer_hand
    elif player_score > dealer_score:
        print("你贏了這一局！\n")
        return "win", player_hand, dealer_hand
    elif player_score < dealer_score:
        print("你輸了這一局！\n")
        return "lose", player_hand, dealer_hand
    else:
        print("這一局平手。\n")
        return "draw", player_hand, dealer_hand

# 多局遊戲（手動 5 勝 3 負）
def play_blackjack_39_series():
    wins = 0
    losses = 0
    round_number = 1

    print("🎮 歡迎來到 39 點智慧 Blackjack（5 勝 3 負制）\n")

    while wins < 5 and losses < 3:
        print(f"=== 第 {round_number} 局 ===")
        result, _, _ = play_one_round(auto_play=False)
        if result == "win":
            wins += 1
        elif result == "lose":
            losses += 1
        print(f"📊 戰績：{wins} 勝 {losses} 敗\n")
        round_number += 1

    print("=== 🎯 遊戲結束 ===")
    if wins >= 5:
        print(f"🎉 恭喜你贏得勝利！最終戰績：{wins} 勝 {losses} 敗")
    else:
        print(f"💀 很遺憾你輸了這場挑戰。最終戰績：{wins} 勝 {losses} 敗")

# 模擬模式：大量自動對戰統計勝率
def simulate_many_games(num_games=1000):
    wins = 0
    losses = 0
    draws = 0
    player_zero = 0
    dealer_zero = 0

    print(f"\n🔁 開始模擬 {num_games} 局自動對戰...\n")

    for i in range(1, num_games + 1):
        print(f"--- 第 {i} 局 ---")
        result, player_hand, dealer_hand = play_one_round(auto_play=True)

        if result == "win":
            wins += 1
        elif result == "lose":
            losses += 1
        else:
            draws += 1

        if sum(card_value(c) for c in player_hand) == 23:
            player_zero += 1
        if sum(card_value(c) for c in dealer_hand) == 23:
            dealer_zero += 1

    # 統計輸出
    print("\n📈 模擬結果統計：")
    print(f"✅ 玩家勝場：{wins}")
    print(f"❌ 玩家敗場：{losses}")
    print(f"➖ 平手次數：{draws}")
    print(f"🎯 玩家觸發 23 歸零次數：{player_zero}")
    print(f"🎯 莊家觸發 23 歸零次數：{dealer_zero}")
    print(f"\n🎯 勝率：{wins / num_games:.2%}")
    print(f"💀 敗率：{losses / num_games:.2%}")
    print(f"⏸️ 平率：{draws / num_games:.2%}")

# 主選單
if __name__ == "__main__":
    print("歡迎來到《39點智慧 Blackjack》")
    print("1. 🎮 手動挑戰模式（5勝3負）")
    print("2. 📊 自動模擬統計勝率")

    mode = input("請選擇模式（1 或 2）：")
    if mode == '1':
        play_blackjack_39_series()
    elif mode == '2':
        count = input("請輸入要模擬的局數（預設 1000）：")
        num = int(count) if count.isdigit() else 1000
        simulate_many_games(num)
    else:
        print("輸入無效，請重新啟動程式。")
