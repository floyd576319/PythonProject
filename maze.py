import tkinter as tk
import random

# 迷宮設定
CELL_SIZE = 40
ROWS = 10
COLS = 10
TRAP_COUNT = 10
MONSTER_COUNT = 5
HP_START = 3

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("迷宮探險 - 圖形版")
        self.canvas = tk.Canvas(master, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()
        self.hp = HP_START

        self.master.bind("<Key>", self.key_press)
        self.restart_game()

    def restart_game(self):
        self.maze = [['.' for _ in range(COLS)] for _ in range(ROWS)]
        self.hp = HP_START
        self.generate_elements()
        self.draw_maze()

    def generate_elements(self):
        # 陷阱
        for _ in range(TRAP_COUNT):
            self.place_random('T')
        # 怪物
        for _ in range(MONSTER_COUNT):
            self.place_random('M')
        # 出口
        self.exit_pos = self.place_random('E')
        # 玩家
        self.player_pos = self.place_random('P')

    def place_random(self, symbol):
        while True:
            x = random.randint(0, ROWS-1)
            y = random.randint(0, COLS-1)
            if self.maze[x][y] == '.':
                self.maze[x][y] = symbol
                return (x, y)

    def draw_maze(self):
        self.canvas.delete("all")
        color_map = {
            '.': "white",
            'P': "blue",
            'T': "orange",
            'M': "red",
            'E': "green"
        }

        for i in range(ROWS):
            for j in range(COLS):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = color_map[self.maze[i][j]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # 顯示血量
        self.canvas.create_text(5, 5, anchor="nw", text=f"血量：{self.hp}", fill="black", font=("Arial", 14))

    def key_press(self, event):
        key = event.keysym
        dx, dy = 0, 0
        if key == "Up":
            dx = -1
        elif key == "Down":
            dx = 1
        elif key == "Left":
            dy = -1
        elif key == "Right":
            dy = 1
        else:
            return

        x, y = self.player_pos
        new_x = x + dx
        new_y = y + dy

        if not (0 <= new_x < ROWS and 0 <= new_y < COLS):
            return  # 超出邊界

        next_cell = self.maze[new_x][new_y]

        if next_cell == 'T':
            self.hp -= 1
        elif next_cell == 'M':
            self.hp -= 1
        elif next_cell == 'E':
            self.canvas.create_text(COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2,
                                    text="成功通關！", fill="green", font=("Arial", 24))
            self.master.after(1500, self.restart_game)
            return

        if self.hp <= 0:
            self.canvas.create_text(COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2,
                                    text="遊戲結束！", fill="red", font=("Arial", 24))
            self.master.unbind("<Key>")
            return

        self.maze[x][y] = '.'
        self.maze[new_x][new_y] = 'P'
        self.player_pos = (new_x, new_y)
        self.draw_maze()

# 執行主程式
if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
