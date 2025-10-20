import random

# === 卡片類別 ===
class Card:
    def __init__(self, name, atk, defe, card_type, effect=None):
        self.name = name
        self.atk = atk
        self.defe = defe
        self.card_type = card_type  # "Monster", "Spell"
        self.effect = effect  # e.g., "boost_atk"
        self.temp_atk_bonus = 0  # for spell effects

    def get_atk(self):
        return self.atk + self.temp_atk_bonus

    def __str__(self):
        if self.card_type == "Monster":
            return f"[{self.name}] ATK: {self.get_atk()} / DEF: {self.defe}"
        elif self.card_type == "Spell":
            return f"[{self.name}] Spell Card - Effect: {self.effect}"
        else:
            return f"[{self.name}] (Unknown Type)"

# === 玩家類別 ===
class Player:
    def __init__(self, name, deck, is_human=False):
        self.name = name
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.hand = []
        self.field = []
        self.LP = 8000
        self.is_human = is_human

    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)
            print(f"{self.name} drew a card: {card.name}")
        else:
            print(f"{self.name} has no more cards to draw!")

    def summon_monster(self):
        monsters_in_hand = [card for card in self.hand if card.card_type == "Monster"]
        if not monsters_in_hand:
            print(f"{self.name} has no monster to summon.")
            return

        if self.is_human:
            print(f"\n{self.name}'s Hand (Monsters):")
            for i, card in enumerate(monsters_in_hand):
                print(f"{i + 1}: {card}")
            try:
                choice = int(input("Choose a monster to summon (by number): ")) - 1
                if 0 <= choice < len(monsters_in_hand):
                    card = monsters_in_hand[choice]
                    self.hand.remove(card)
                    self.field.append(card)
                    print(f"{self.name} summoned {card.name}!")
                else:
                    print("Invalid choice. No monster summoned.")
            except ValueError:
                print("Invalid input. No monster summoned.")
        else:
            card = monsters_in_hand[0]
            self.hand.remove(card)
            self.field.append(card)
            print(f"{self.name} summoned {card.name}.")

    def activate_spell(self):
        spells_in_hand = [card for card in self.hand if card.card_type == "Spell"]
        if not spells_in_hand:
            return

        if self.is_human:
            print(f"\n{self.name}'s Hand (Spells):")
            for i, card in enumerate(spells_in_hand):
                print(f"{i + 1}: {card}")
            use = input("Do you want to use a Spell card? (y/n): ").lower()
            if use == 'y':
                try:
                    choice = int(input("Choose a spell to use (by number): ")) - 1
                    if 0 <= choice < len(spells_in_hand):
                        spell = spells_in_hand[choice]
                        self.hand.remove(spell)
                        self.use_spell_effect(spell)
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
        else:
            # AI自動使用第一張魔法卡，如果有怪獸可用
            spell = spells_in_hand[0]
            if spell.effect == "boost_atk" and self.field:
                self.hand.remove(spell)
                self.use_spell_effect(spell)

    def use_spell_effect(self, spell):
        if spell.effect == "boost_atk":
            targets = [card for card in self.field if card.card_type == "Monster"]
            if not targets:
                print(f"{self.name} has no monsters to use {spell.name} on.")
                return

            if self.is_human:
                print(f"\nChoose a monster to boost:")
                for i, card in enumerate(targets):
                    print(f"{i + 1}: {card}")
                try:
                    choice = int(input("Your choice: ")) - 1
                    if 0 <= choice < len(targets):
                        target = targets[choice]
                        target.temp_atk_bonus += 500
                        print(f"{target.name} gains +500 ATK!")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
            else:
                target = targets[0]
                target.temp_atk_bonus += 500
                print(f"{self.name} used {spell.name} on {target.name} (+500 ATK).")

# === 戰鬥邏輯 ===
def battle(attacker, defender):
    if not attacker.field:
        print(f"{attacker.name} has no monsters to attack with!")
        return

    atk_card = attacker.field[0]

    if not defender.field:
        damage = atk_card.get_atk()
        defender.LP -= damage
        print(f"{attacker.name}'s {atk_card.name} attacks directly for {damage} damage!")
        return

    if attacker.is_human:
        print(f"\n{defender.name}'s Field:")
        for i, card in enumerate(defender.field):
            print(f"{i + 1}: {card}")
        try:
            choice = int(input("Choose a monster to attack (by number): ")) - 1
            if 0 <= choice < len(defender.field):
                def_card = defender.field[choice]
            else:
                print("Invalid choice. Skipping battle.")
                return
        except ValueError:
            print("Invalid input. Skipping battle.")
            return
    else:
        def_card = defender.field[0]

    print(f"{attacker.name}'s {atk_card.name} (ATK {atk_card.get_atk()}) attacks {defender.name}'s {def_card.name} (ATK {def_card.get_atk()})")

    if atk_card.get_atk() > def_card.get_atk():
        damage = atk_card.get_atk() - def_card.get_atk()
        defender.LP -= damage
        defender.field.remove(def_card)
        print(f"{def_card.name} is destroyed! {defender.name} takes {damage} damage.")
    elif atk_card.get_atk() < def_card.get_atk():
        damage = def_card.get_atk() - atk_card.get_atk()
        attacker.LP -= damage
        attacker.field.remove(atk_card)
        print(f"{atk_card.name} is destroyed! {attacker.name} takes {damage} damage.")
    else:
        attacker.field.remove(atk_card)
        defender.field.remove(def_card)
        print("Both monsters are destroyed in a draw!")

# === 主遊戲迴圈 ===
def game_loop(player1, player2):
    turn = 0
    print("=== Duel Start! ===")
    while player1.LP > 0 and player2.LP > 0:
        attacker = player1 if turn % 2 == 0 else player2
        defender = player2 if turn % 2 == 0 else player1

        print(f"\n===== Turn {turn + 1}: {attacker.name}'s Turn =====")
        attacker.draw_card()
        attacker.activate_spell()
        attacker.summon_monster()
        battle(attacker, defender)

        print(f"{player1.name} LP: {player1.LP} / {player2.name} LP: {player2.LP}")
        turn += 1

        if player1.LP <= 0 and player2.LP <= 0:
            print("\n💥 Both duelists have fallen! It's a draw!")
            return

    winner = player1 if player1.LP > 0 else player2
    print(f"\n🏆 {winner.name} wins the duel!")

# === 建立牌組 ===
def create_sample_deck():
    return [
        Card("Blue-Eyes White Dragon", 3000, 2500, "Monster"),
        Card("Dark Magician", 2500, 2100, "Monster"),
        Card("Summoned Skull", 2500, 1200, "Monster"),
        Card("Celtic Guardian", 1400, 1200, "Monster"),
        Card("Mystical Elf", 800, 2000, "Monster"),
        Card("La Jinn the Mystical Genie", 1800, 1000, "Monster"),
        Card("Battle Ox", 1700, 1000, "Monster"),
        Card("Axe Raider", 1700, 1150, "Monster"),
        Card("Harpie Lady", 1300, 1400, "Monster"),
        Card("Giant Soldier of Stone", 1300, 2000, "Monster"),
        Card("Power Boost", 0, 0, "Spell", effect="boost_atk"),
        Card("Power Boost", 0, 0, "Spell", effect="boost_atk"),
    ] * 1  # 每張一張，共 12 張

# === 執行遊戲 ===
if __name__ == "__main__":
    deck1 = create_sample_deck()
    deck2 = create_sample_deck()

    player1 = Player("You", deck1, is_human=True)
    player2 = Player("Kaiba (AI)", deck2, is_human=False)

    game_loop(player1, player2)
