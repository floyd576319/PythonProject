import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.is_joker = (suit is None)
        self.is_little_joker = (suit == '小')
        self.is_little_joker_remover = (suit == '除小')
        self.disguised_rank = None
        self.has_bomb_tag = False
        self.has_landmine_tag = False
        self.is_sealed = False
        self.seal_rounds = 0
        self.is_bomb_hidden = False

    def __str__(self):
        label = ''
        if self.is_sealed:
            label = f'被封印的'
        elif self.is_joker and self.disguised_rank:
            label = f'偽裝過的 {self.disguised_rank}'
        elif self.is_joker:
            label = self.rank
        elif self.is_little_joker:
            label = '小鬼牌'
        elif self.is_little_joker_remover:
            label = '除小鬼牌'
        else:
            label = f'{self.suit}{self.rank}'

        if self.has_bomb_tag and not self.is_bomb_hidden:
            return f'{label} (炸彈)'
        if self.has_landmine_tag:
            return f'{label} (地雷)'
        return label


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.is_human = (name == '你')
        self.has_strategy = (name != '你')
        self.special_ability_uses = 3 if name in ['電腦 1', '電腦 3', '電腦 4', '電腦 5', '電腦 6'] else 0
        self.is_disguised = False
        self.triplet_pair = False
        self.has_little_joker_ability = (name == '你')
        self.is_out = False
        self.is_skipped = False
        self.sealed_card = None
        self.is_revealed_to_pc6 = False
        self.ability_sealed_rounds = 0

        # 電腦2的特殊能力獨立計算
        self.joker_disguise_uses = 3 if name == '電腦 2' else 0
        self.bomb_hide_uses = 3 if name == '電腦 2' else 0
        self.known_disguised_cards = []
        self.known_hidden_bombs = []

        # 玩家的新能力，只由這個屬性追蹤次數
        self.gained_ability = None
        self.player_ability_uses = 3 if self.is_human else 0
        self.is_using_pc1_ability = False
        self.can_re_use_landmine_ability = False

    def receive_card(self, card):
        self.hand.append(card)

    def sort_hand(self):
        normal_cards = sorted([card for card in self.hand if card.suit is not None and card.suit not in ['小', '除小']],
                              key=lambda card: card.rank)
        jokers = [card for card in self.hand if
                  card.is_joker and not card.is_little_joker and not card.is_little_joker_remover]
        little_jokers = [card for card in self.hand if card.is_little_joker]
        little_joker_removers = [card for card in self.hand if card.is_little_joker_remover]
        self.hand = normal_cards + jokers + little_jokers + little_joker_removers

    def find_and_remove_pairs(self):
        self.sort_hand()
        new_hand = []
        i = 0
        removed_pairs = []

        while i < len(self.hand) - 1:
            if self.hand[i].is_sealed:
                new_hand.append(self.hand[i])
                i += 1
                continue

            if self.hand[i].is_little_joker_remover:
                for j in range(len(self.hand)):
                    if self.hand[j].is_little_joker and not self.hand[j].is_sealed:
                        removed_pairs.append('小鬼牌')
                        removed_pairs.append('除小鬼牌')
                        self.hand.pop(j)
                        self.hand.pop(i)
                        self.find_and_remove_pairs()
                        return
                new_hand.append(self.hand[i])
                i += 1
                continue

            if self.hand[i].is_little_joker:
                if i < len(self.hand) - 2 and self.hand[i + 1].is_little_joker and self.hand[i + 2].is_little_joker:
                    removed_pairs.append('小鬼牌')
                    i += 3
                else:
                    new_hand.append(self.hand[i])
                    i += 1
                continue

            if self.triplet_pair:
                if i < len(self.hand) - 2 and self.hand[i].suit is not None and self.hand[i].rank == self.hand[
                    i + 1].rank and self.hand[i].rank == self.hand[i + 2].rank:
                    removed_pairs.append(self.hand[i].rank)
                    i += 3
                else:
                    new_hand.append(self.hand[i])
                    i += 1
            else:
                if self.hand[i].suit is not None and self.hand[i].rank == self.hand[i + 1].rank:
                    removed_pairs.append(self.hand[i].rank)
                    i += 2
                else:
                    new_hand.append(self.hand[i])
                    i += 1

        if i == len(self.hand) - 1:
            new_hand.append(self.hand[i])

        self.hand = new_hand
        if removed_pairs:
            print_text = f'{self.name} 丟棄了 '
            if '小鬼牌' in removed_pairs:
                print_text += f'一組除小鬼牌和小鬼牌，'
            if '小鬼牌' in removed_pairs and removed_pairs.count('小鬼牌') > 1:
                print_text += f'{removed_pairs.count("小鬼牌") - 1} 組小鬼牌三條，'

            normal_pairs = [r for r in removed_pairs if r != '小鬼牌' and r != '除小鬼牌']
            if normal_pairs:
                if self.triplet_pair:
                    print_text += f'{len(normal_pairs)} 組三條： {", ".join(normal_pairs)}。'
                    self.triplet_pair = False
                else:
                    print_text += f'{len(normal_pairs)} 組對子： {", ".join(normal_pairs)}。'

            print(print_text)

    def adjust_hand_order(self):
        if not self.is_human:
            return

        print(f'\n你的手牌目前順序是：')
        print([f'{i}: {str(card)}' for i, card in enumerate(self.hand)])

        choice = input('是否要調整手牌順序？(Y/N): ').strip().upper()
        if choice == 'Y':
            while True:
                new_order_input = input(f'請輸入新的順序（0 到 {len(self.hand) - 1} 的數字，以空格分隔）：').strip()
                try:
                    new_order = [int(x) for x in new_order_input.split()]
                    if len(new_order) == len(self.hand) and sorted(new_order) == list(range(len(self.hand))):
                        new_hand = [self.hand[i] for i in new_order]
                        self.hand = new_hand
                        print('手牌順序已調整。')
                        break
                    else:
                        print('輸入的順序不正確，請重新輸入。')
                except (ValueError, IndexError):
                    print('輸入格式錯誤，請確保輸入的是以空格分隔的有效數字。')

    def disguise_and_hide_permanently(self):
        jokers = [card for card in self.hand if card.is_joker and not card.is_little_joker and not card.disguised_rank]
        if jokers:
            joker_to_disguise = random.choice(jokers)
            normal_ranks = [card.rank for card in self.hand if
                            not card.is_joker and not card.is_little_joker and not card.is_little_joker_remover]

            if normal_ranks:
                joker_to_disguise.disguised_rank = random.choice(normal_ranks)
            else:
                ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                joker_to_disguise.disguised_rank = random.choice(ranks)

            self.known_disguised_cards.append(joker_to_disguise)
            if self.is_human:
                print(f'你發動了電腦 2 的鬼牌偽裝能力！')
            else:
                self.joker_disguise_uses -= 1
                print(f'電腦 2 秘密發動了鬼牌偽裝能力！')

        bomb_cards = [card for card in self.hand if card.has_bomb_tag and not card.is_bomb_hidden]
        if bomb_cards:
            card_to_hide = random.choice(bomb_cards)
            card_to_hide.is_bomb_hidden = True
            self.known_hidden_bombs.append(card_to_hide)
            if self.is_human:
                print(f'你發動了電腦 2 的炸彈標籤隱藏能力！')
            else:
                self.bomb_hide_uses -= 1
                print(f'電腦 2 秘密地隱藏了炸彈標籤。')

    def restore_all(self):
        for card in self.known_disguised_cards:
            if card in self.hand:
                card.disguised_rank = None
        for card in self.known_hidden_bombs:
            if card in self.hand:
                card.is_bomb_hidden = False

        self.known_disguised_cards = []
        self.known_hidden_bombs = []

    def set_bomb_tags(self):
        un_tagged_cards = [card for card in self.hand if not card.has_bomb_tag and not card.has_landmine_tag]
        if self.special_ability_uses > 0 and len(un_tagged_cards) >= 3 and self.ability_sealed_rounds == 0:
            cards_to_tag = random.sample(un_tagged_cards, 3)
            for card in cards_to_tag:
                card.has_bomb_tag = True
            self.special_ability_uses -= 1
            print(f'電腦 4 秘密地為三張牌貼上了炸彈標籤。')
            return True
        return False

    def set_landmine_tags(self):
        un_tagged_cards = [card for card in self.hand if not card.has_bomb_tag and not card.has_landmine_tag]
        if len(un_tagged_cards) >= 3:
            cards_to_tag = random.sample(un_tagged_cards, 3)
            for card in cards_to_tag:
                card.has_landmine_tag = True
            print(f'你發動了地雷能力！為三張牌貼上了地雷標籤。')
            return True
        return False

    def check_for_bomb_tags(self, players):
        if self.name == '電腦 4':
            return False

        bomb_cards = [card for card in self.hand if card.has_bomb_tag]
        if len(bomb_cards) >= 3:
            print(f'\n{self.name} 湊齊了三張炸彈牌！{self.name} 爆炸了，被淘汰出局！')
            self.is_out = True
            self.hand = []

            pc4 = next((p for p in players if p.name == '電腦 4'), None)
            if pc4:
                pc4.special_ability_uses += 1
                print(f'電腦 4 成功讓對手因炸彈標籤淘汰，並獲得了一次額外的特殊能力使用次數。')
            return True
        return False

    def check_for_landmine_tags(self, players):
        if self.is_human:
            return None

        landmine_cards = [card for card in self.hand if card.has_landmine_tag]
        if len(landmine_cards) >= 3:
            print(f'\n{self.name} 湊齊了三張地雷牌！{self.name} 爆炸了，被淘汰出局！')
            self.is_out = True
            self.hand = []

            human_player = next((p for p in players if p.is_human), None)
            if human_player:
                human_player.can_re_use_landmine_ability = True
                print(f'你成功用地雷標籤淘汰了 {self.name}！')
            return self.name
        return None

    def seal_card(self):
        unsealed_cards = [card for card in self.hand if not card.is_sealed]
        if not unsealed_cards:
            return None

        card_to_seal = None
        jokers = [card for card in unsealed_cards if (card.is_joker or card.is_little_joker)]
        if jokers:
            card_to_seal = random.choice(jokers)
        else:
            high_value_ranks = ['A', 'K', 'Q', 'J']
            high_value_cards = [card for card in unsealed_cards if card.rank in high_value_ranks]
            if high_value_cards:
                card_to_seal = random.choice(high_value_cards)
            else:
                card_to_seal = random.choice(unsealed_cards)

        if card_to_seal:
            card_to_seal.is_sealed = True
            card_to_seal.seal_rounds = 2
            self.sealed_card = card_to_seal
            return card_to_seal
        return None

    def seal_player_ability(self, players):
        eligible_players = [p for p in players if
                            p != self and p.has_cards() and p.name not in ['電腦 5'] and p.ability_sealed_rounds == 0]
        if not eligible_players:
            return None

        # 策略性選擇目標
        # 優先封印手牌多的玩家
        target_player = max(eligible_players, key=lambda p: len(p.hand))

        # 如果電腦6在場上且手牌數和最強玩家相近，優先封印電腦6
        pc6 = next((p for p in eligible_players if p.name == '電腦 6'), None)
        if pc6 and len(pc6.hand) >= len(target_player.hand) - 2:
            target_player = pc6

        target_player.ability_sealed_rounds = 4
        return target_player

    def update_seal_rounds(self):
        if self.sealed_card and self.sealed_card.is_sealed:
            self.sealed_card.seal_rounds -= 1
            if self.sealed_card.seal_rounds <= 0:
                self.sealed_card.is_sealed = False
                self.sealed_card = None
                if self.is_human:
                    print(f'你的卡牌封印能力已失效。')
                else:
                    print(f'電腦 5 的卡牌封印能力已失效。')

    def reveal_hand_to_pc6(self, players):
        if self.name == '電腦 6' and self.special_ability_uses > 0 and self.ability_sealed_rounds == 0:

            target_players = [p for p in players if p != self and p.has_cards() and not p.is_revealed_to_pc6]
            if not target_players:
                return

            prioritized_names = ['你', '電腦 2', '電腦 3', '電腦 4']
            target_player = None

            for name in prioritized_names:
                if any(p.name == name for p in target_players):
                    target_player = next(p for p in target_players if p.name == name)
                    break

            if target_player is None:
                target_player = max(target_players, key=lambda p: len(p.hand))

            if target_player:
                target_player.is_revealed_to_pc6 = True
                if target_player.is_human:
                    target_player.player_ability_uses = 5
                else:
                    target_player.special_ability_uses = 5
                self.special_ability_uses -= 1
                print(f'電腦 6 發動了特殊能力！指定了 {target_player.name}，該玩家的特殊能力使用次數變為 5 次。')
                print(f'作為代價，{target_player.name} 的手牌資訊對電腦 6 是公開的。')
                return True
        return False

    def get_revealed_hand_info(self, players):
        if self.name == '電腦 6':
            for player in players:
                if player.is_revealed_to_pc6:
                    print(f'電腦 6 觀察到 {player.name} 的手牌是：{[str(card) for card in player.hand]}')

    def has_cards(self):
        return len(self.hand) > 0 and not self.is_out

    def draw_card_from(self, other_player, players):
        card_to_draw = -1

        if self.is_human:
            if self.is_using_pc1_ability and len(other_player.hand) >= 2:
                print(
                    f'\n你正在使用電腦 1 的能力！你看到 {other_player.name} 手牌最左邊是 {other_player.hand[0]}，最右邊是 {other_player.hand[-1]}。')

            print(f'\n你的手牌是： {[str(card) for card in self.hand]}')
            print(f'{other_player.name} 有 {len(other_player.hand)} 張牌。')
            while card_to_draw not in range(len(other_player.hand)):
                try:
                    card_to_draw = int(
                        input(f'請從 {other_player.name} 的手牌中選一張（0 到 {len(other_player.hand) - 1}）：'))
                except ValueError:
                    print('請輸入有效的數字。')

            self.is_using_pc1_ability = False
        else:
            if self.name == '電腦 6' and other_player.is_revealed_to_pc6:
                joker_indices = [i for i, card in enumerate(other_player.hand) if card.is_joker]
                available_indices = [i for i in range(len(other_player.hand)) if i not in joker_indices]
                if available_indices:
                    card_to_draw = random.choice(available_indices)
                else:
                    card_to_draw = random.randint(0, len(other_player.hand) - 1)
            elif self.name == '電腦 1' and self.special_ability_uses > 0 and self.ability_sealed_rounds == 0 and 2 <= len(
                    other_player.hand) <= 4:
                print(f'{self.name} 秘密發動了特殊能力...')
                left_card = other_player.hand[0]
                right_card = other_player.hand[-1]
                self.special_ability_uses -= 1

                avoid_indices = []
                if left_card.is_joker:
                    avoid_indices.append(0)
                if right_card.is_joker and len(other_player.hand) > 1:
                    avoid_indices.append(len(other_player.hand) - 1)

                available_to_draw_indices = [i for i in range(len(other_player.hand)) if i not in avoid_indices]
                if available_to_draw_indices:
                    card_to_draw = random.choice(available_to_draw_indices)
                else:
                    card_to_draw = random.randint(0, len(other_player.hand) - 1)
            elif self.name == '電腦 2':
                known_cards = self.known_disguised_cards + self.known_hidden_bombs
                available_indices = [i for i, card in enumerate(other_player.hand) if card not in known_cards]
                if available_indices:
                    card_to_draw = random.choice(available_indices)
                else:
                    card_to_draw = random.randint(0, len(other_player.hand) - 1)
            else:
                if card_to_draw == -1:
                    if other_player.is_human or not other_player.has_strategy:
                        card_to_draw = random.randint(0, len(other_player.hand) - 1)
                    else:
                        my_ranks = {card.rank for card in self.hand}
                        available_to_draw_indices = []
                        for i, card in enumerate(other_player.hand):
                            if not card.is_joker and not card.is_little_joker and not card.is_little_joker_remover and card.rank not in my_ranks:
                                available_to_draw_indices.append(i)

                        if available_to_draw_indices:
                            card_to_draw = random.choice(available_to_draw_indices)
                        else:
                            card_to_draw = random.randint(0, len(other_player.hand) - 1)

            print(f'{self.name} 從 {other_player.name} 抽了一張牌。')

        drawn_card = other_player.hand.pop(card_to_draw)
        if self.is_human:
            print(f'你抽到了 {drawn_card}。')
        self.hand.append(drawn_card)
        self.find_and_remove_pairs()

        if self.check_for_bomb_tags(players):
            return True
        if self.check_for_landmine_tags(players):
            return True
        return False

    def __str__(self):
        return self.name


def check_and_refill_cards(players):
    all_cards = []
    for player in players:
        if player.has_cards():
            all_cards.extend([card for card in player.hand if
                              not card.is_joker and not card.is_little_joker and not card.is_little_joker_remover])

    # 計算每種點數的牌數
    rank_counts = {}
    for card in all_cards:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

    # 檢查是否有無法配對的單張牌
    for player in players:
        if player.has_cards():
            for card in player.hand:
                if not card.is_joker and not card.is_little_joker and not card.is_little_joker_remover:
                    if rank_counts.get(card.rank) == 1:
                        suits = ['♠', '♥', '♦', '♣']
                        available_suits = [s for s in suits if s != card.suit]

                        if available_suits:
                            new_suit = random.choice(available_suits)
                            new_card = Card(new_suit, card.rank)
                            player.receive_card(new_card)
                            print(
                                f'\n【系統公告】: 偵測到 {player.name} 手中有無法配對的 {card.rank}，已自動補上一張 {new_card}。')
                            player.find_and_remove_pairs()
                            return True
    return False


def pc5_strategy_choice(current_player, players):
    """
    電腦5的策略選擇函數，用於判斷發動哪種能力
    """
    # 策略性選擇目標
    other_players_with_cards = [p for p in players if p.name != current_player.name and p.has_cards() and not p.is_out]
    if not other_players_with_cards:
        return 1  # 如果沒有其他玩家，只能封印自己手牌

    # 檢查是否有鬼牌或高價值牌需要保護
    jokers = [c for c in current_player.hand if c.is_joker or c.is_little_joker]
    high_value_cards = [c for c in current_player.hand if c.rank in ['A', 'K', 'Q', 'J']]
    has_valuable_card = len(jokers) > 0 or len(high_value_cards) > 0

    # 檢查是否有值得封印的玩家能力
    has_high_card_player = False
    max_cards = 0
    if other_players_with_cards:
        max_cards = max(len(p.hand) for p in other_players_with_cards)

    if max_cards >= len(current_player.hand) + 2:
        has_high_card_player = True

    pc6_exists = any(p.name == '電腦 6' and p.ability_sealed_rounds == 0 for p in other_players_with_cards)

    # 做出最終選擇
    if has_high_card_player or pc6_exists:
        return 2  # 封印玩家能力
    else:
        return 1  # 封印卡牌


def setup_game():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [Card(suit, rank) for suit in suits for rank in ranks]

    deck.append(Card(None, '鬼牌A'))
    deck.append(Card(None, '鬼牌B'))

    random.shuffle(deck)

    players = [Player('你'), Player('電腦 1'), Player('電腦 2'), Player('電腦 3'), Player('電腦 4'), Player('電腦 5'),
               Player('電腦 6')]

    for i, card in enumerate(deck):
        players[i % len(players)].receive_card(card)

    print('--- 遊戲開始！發牌中 ---')
    for player in players:
        player.find_and_remove_pairs()

    return players


def play_game():
    players = setup_game()
    current_player_index = 0
    rankings = []

    while sum(1 for p in players if p.has_cards()) > 1:
        while check_and_refill_cards(players):
            pass

        current_player = players[current_player_index]

        if current_player.is_out:
            current_player_index = (current_player_index + 1) % len(players)
            continue

        for p in players:
            if p.ability_sealed_rounds > 0:
                p.ability_sealed_rounds -= 1
                if p.ability_sealed_rounds == 0:
                    print(f'{p.name} 的特殊能力封印已解除。')

            p.update_seal_rounds()

        active_players_count = sum(1 for p in players if p.has_cards())
        if active_players_count == 2:
            print('\n--- 遊戲只剩下兩位玩家，所有偽裝和隱藏效果將解除 ---')
            for p in players:
                if p.name == '電腦 2':
                    p.restore_all()

        if current_player.is_skipped:
            print(f'{current_player.name} 的回合被跳過了！')
            current_player.is_skipped = False
            current_player_index = (current_player_index + 1) % len(players)
            continue

        if current_player.has_cards():
            # 人類玩家的特殊能力發動
            if current_player.is_human:
                current_player.adjust_hand_order()

                chain_reaction = False
                if current_player.can_re_use_landmine_ability:
                    current_player.gained_ability = 4
                    current_player.can_re_use_landmine_ability = False
                    print('\n你成功用地雷能力淘汰了對手！現在可以再次發動地雷能力。')
                    chain_reaction = True

                if current_player.player_ability_uses > 0 and current_player.ability_sealed_rounds == 0 and not chain_reaction:
                    roll_choice = input(
                        f'\n你還有 {current_player.player_ability_uses} 次發動特殊能力的機會，是否要擲骰子？(Y/N): ').strip().upper()
                    if roll_choice == 'Y':
                        dice_roll = random.randint(1, 6)
                        current_player.gained_ability = dice_roll
                        current_player.player_ability_uses -= 1
                        print(f'你擲出了 {dice_roll} 點！你獲得了使用電腦 {dice_roll} 的特殊能力。')

                if current_player.gained_ability is not None and current_player.ability_sealed_rounds == 0:
                    use_ability_choice = 'Y' if chain_reaction else input(
                        f'你目前獲得了電腦 {current_player.gained_ability} 的能力，是否要現在使用？(Y/N): ').strip().upper()
                    if use_ability_choice == 'Y':
                        dice_roll = current_player.gained_ability
                        if dice_roll == 1:
                            print(f'你發動了電腦 1 的能力！本回合抽牌前你將能看到對手最左和最右的牌。')
                            current_player.is_using_pc1_ability = True
                            print(f'你已經使用完該次電腦 1 特殊能力的機會。')
                        elif dice_roll == 2:
                            current_player.disguise_and_hide_permanently()
                            print(f'你已經使用完該次電腦 2 特殊能力的機會。')
                        elif dice_roll == 3:
                            eligible_players = [p for p in players if
                                                p != current_player and p.has_cards() and 2 <= len(p.hand) <= 4]
                            if eligible_players:
                                target_player = random.choice(eligible_players)
                                target_player.is_skipped = True
                                print(f'你發動了電腦 3 的能力！指定 {target_player.name} 的下一回合將被跳過。')
                                print(f'你已經使用完該次電腦 3 特殊能力的機會。')
                            else:
                                print('無法發動電腦 3 的能力。')
                        elif dice_roll == 4:
                            if current_player.set_landmine_tags():
                                print(f'你已經使用完該次地雷特殊能力的機會。')
                            else:
                                print('無法發動地雷特殊能力，因為你沒有足夠的牌來貼上標籤。')
                        elif dice_roll == 5:
                            if len(current_player.hand) > 0:
                                # 人類玩家使用電腦5能力時，系統自動選擇
                                choice = pc5_strategy_choice(current_player, players)

                                if choice == 1:
                                    sealed_card = current_player.seal_card()
                                    if sealed_card:
                                        print(f'你發動了卡牌封印能力，將 {sealed_card} 封印了兩個回合！')
                                elif choice == 2:
                                    target = current_player.seal_player_ability(players)
                                    if target:
                                        print(f'你發動了玩家能力封印，指定 {target.name} 四回合內無法使用特殊能力！')
                                    else:
                                        print('無法發動能力，沒有合適的目標。')

                                print(f'你已經使用完該次電腦 5 特殊能力的機會。')
                            else:
                                print('無法發動電腦 5 的能力。')
                        elif dice_roll == 6:
                            eligible_players = [p for p in players if
                                                p != current_player and p.has_cards() and not p.is_revealed_to_pc6]
                            if eligible_players:
                                target_player = max(eligible_players, key=lambda p: len(p.hand))
                                target_player.is_revealed_to_pc6 = True
                                if target_player.is_human:
                                    target_player.player_ability_uses = 5
                                else:
                                    target_player.special_ability_uses = 5
                                print(
                                    f'你發動了電腦 6 的能力！指定了 {target_player.name}，該玩家的特殊能力使用次數變為 5 次。')
                                print(f'作為代價，{target_player.name} 的手牌資訊對你而言是公開的。')
                                print(f'你已經使用完該次電腦 6 特殊能力的機會。')
                            else:
                                print('無法發動電腦 6 的能力。')
                        current_player.gained_ability = None

                # 如果玩家的特殊能力被封印了
                if current_player.ability_sealed_rounds > 0:
                    print(f'你的特殊能力被封印了，還有 {current_player.ability_sealed_rounds} 回合才能使用。')

            # 電腦玩家的特殊能力發動
            if current_player.ability_sealed_rounds == 0:
                if current_player.name == '電腦 2':
                    if (current_player.joker_disguise_uses > 0 and any(c.is_joker for c in current_player.hand)) or \
                            (current_player.bomb_hide_uses > 0 and any(c.has_bomb_tag for c in current_player.hand)):
                        current_player.disguise_and_hide_permanently()

                if current_player.name == '電腦 3' and current_player.special_ability_uses > 0:
                    eligible_players = [p for p in players if
                                        p != current_player and p.has_cards() and 2 <= len(p.hand) <= 4]
                    if eligible_players:
                        target_player = random.choice(eligible_players)
                        target_player.is_skipped = True
                        current_player.special_ability_uses -= 1
                        print(f'電腦 3 發動了特殊能力！指定 {target_player.name} 的下一回合將被跳過。')

                if current_player.name == '電腦 4' and current_player.special_ability_uses > 0:
                    if len(current_player.hand) >= 5 or current_player.special_ability_uses == 3:
                        if current_player.set_bomb_tags():
                            print(f'電腦 4 秘密地為三張牌貼上了炸彈標籤。')

                if current_player.name == '電腦 5' and current_player.special_ability_uses > 0:
                    if len(current_player.hand) >= 5 or current_player.special_ability_uses == 3:
                        choice = pc5_strategy_choice(current_player, players)

                        if choice == 1:
                            sealed_card = current_player.seal_card()
                            if sealed_card:
                                current_player.special_ability_uses -= 1
                                print(f'電腦 5 發動了卡牌封印能力，將 {sealed_card} 封印了兩個回合。')
                        elif choice == 2:
                            target = current_player.seal_player_ability(players)
                            if target:
                                current_player.special_ability_uses -= 1
                                print(f'電腦 5 發動了玩家能力封印，指定 {target.name} 四回合內無法使用特殊能力。')

                # 在電腦6的回合開始時，檢查並發動其能力
                if current_player.name == '電腦 6':
                    current_player.reveal_hand_to_pc6(players)
                    current_player.get_revealed_hand_info(players)
            else:
                print(
                    f'{current_player.name} 的特殊能力被封印，無法使用。還有 {current_player.ability_sealed_rounds} 回合解除。')

            next_player_index = (current_player_index + 1) % len(players)
            next_player = players[next_player_index]

            while not next_player.has_cards() or next_player.is_out:
                next_player_index = (next_player_index + 1) % len(players)
                next_player = players[next_player_index]

            if next_player.has_cards():
                if current_player.draw_card_from(next_player, players):
                    continue

                if not current_player.has_cards():
                    print(f'\n恭喜 {current_player.name}，手牌都出完了！')
                    rankings.append(current_player.name)

        current_player_index = (current_player_index + 1) % len(players)

    remaining_player = next((p for p in players if p.has_cards()), None)
    if remaining_player and not remaining_player.is_out:
        print(f'\n最後剩下 {remaining_player.name}，手牌中還有鬼牌，因此他就是輸家！')
        rankings.append(remaining_player.name)

    print("\n--- 遊戲結束！最終排名 ---")
    for i, name in enumerate(rankings):
        print(f'第 {i + 1} 名： {name}')


if __name__ == '__main__':
    play_game()