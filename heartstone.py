import pygame
import random
import sys
import time

# 初始化 Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("arial", 20)
CLOCK = pygame.time.Clock()

# 顏色定義
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BG_COLOR = (50, 100, 50)

# 卡牌物件
class Card:
    def __init__(self, name, atk, hp, cost):
        self.name = name
        self.attack = atk
        self.health = hp
        self.cost = cost
        self.rect = pygame.Rect(0, 0, 80, 100)

    def draw(self, x, y):
        self.rect.topleft = (x, y)
        pygame.draw.rect(SCREEN, GRAY, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)
        SCREEN.blit(FONT.render(self.name, True, BLACK), (x + 5, y + 5))
        SCREEN.blit(FONT.render(f"ATK:{self.attack}", True, RED), (x + 5, y + 30))
        SCREEN.blit(FONT.render(f"HP:{self.health}", True, BLUE), (x + 5, y + 50))
        SCREEN.blit(FONT.render(f"COST:{self.cost}", True, GREEN), (x + 5, y + 75))

# 玩家物件
class Player:
    def __init__(self, name, y_pos):
        self.name = name
        self.hp = 30
        self.mana = 1
        self.max_mana = 1
        self.hand = []
        self.board = []
        self.y_pos = y_pos

    def draw_ui(self):
        pygame.draw.rect(SCREEN, WHITE, (10, self.y_pos, 200, 40))
        SCREEN.blit(FONT.render(f"{self.name} HP:{self.hp} Mana:{self.mana}/{self.max_mana}", True, BLACK), (15, self.y_pos + 10))

    def draw_hand(self):
        for i, card in enumerate(self.hand):
            card.draw(100 + i * 90, self.y_pos + 50)

    def draw_board(self):
        for i, card in enumerate(self.board):
            card.draw(100 + i * 90, self.y_pos + 180)

    def random_card(self):
        names = ["狼", "龍", "盾兵", "戰士"]
        return Card(random.choice(names), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5))

    def draw_card(self):
        if len(self.hand) < 5:
            self.hand.append(self.random_card())

    def start_turn(self):
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        self.draw_card()

# 初始雙方
player = Player("玩家", 300)
enemy = Player("電腦", 0)
turn_player = player
waiting_player = enemy
turn = 1
game_over = False

def draw_screen():
    SCREEN.fill(BG_COLOR)
    player.draw_ui()
    player.draw_hand()
    player.draw_board()
    enemy.draw_ui()
    enemy.draw_board()
    if game_over:
        pygame.draw.rect(SCREEN, WHITE, (250, 250, 300, 100))
        winner = "玩家" if enemy.hp <= 0 else "電腦"
        SCREEN.blit(FONT.render(f"🏆 {winner} 勝利！", True, RED), (300, 290))
    pygame.display.update()

def do_auto_attack(attacker, defender):
    for card in attacker.board:
        if defender.board:
            target = defender.board[0]
            target.health -= card.attack
            card.health -= target.attack
            if target.health <= 0:
                defender.board.remove(target)
            if card.health <= 0:
                attacker.board.remove(card)
        else:
            defender.hp -= card.attack

def ai_turn():
    print("[電腦回合]")
    enemy.start_turn()
    time.sleep(1)
    for card in enemy.hand[:]:
        if card.cost <= enemy.mana:
            enemy.board.append(card)
            enemy.hand.remove(card)
            enemy.mana -= card.cost
            print(f"電腦打出 {card.name}")
            time.sleep(0.5)
    do_auto_attack(enemy, player)

def switch_turn():
    global turn_player, waiting_player
    turn_player, waiting_player = waiting_player, turn_player

# 主迴圈
def main():
    global game_over
    player.start_turn()
    draw_screen()
    while True:
        draw_screen()
        if turn_player == enemy and not game_over:
            ai_turn()
            if player.hp <= 0:
                game_over = True
            else:
                switch_turn()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                for card in turn_player.hand:
                    if card.rect.collidepoint(pos):
                        if card.cost <= turn_player.mana:
                            turn_player.hand.remove(card)
                            turn_player.board.append(card)
                            turn_player.mana -= card.cost
                            print(f"{turn_player.name} 出牌 {card.name}")

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    # 結束回合
                    do_auto_attack(turn_player, waiting_player)
                    if waiting_player.hp <= 0:
                        game_over = True
                    else:
                        switch_turn()
                        turn_player.start_turn()

        CLOCK.tick(30)

main()
