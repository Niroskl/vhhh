import tkinter as tk
import random
from functools import partial

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("משחק זיכרון")
        self.buttons = []
        self.first = None
        self.second = None
        self.lock = False  # מונע לחיצות בזמן בדיקה
        self.matches = 0
        
        # רשימת ערכים - 8 זוגות
        self.values = list(range(1, 9)) * 2
        random.shuffle(self.values)
        
        self.create_board()

    def create_board(self):
        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.root, text="?", width=6, height=3, 
                                command=partial(self.on_click, i*4 + j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

    def on_click(self, index):
        if self.lock:
            return
        btn = self.buttons[index]
        if btn["text"] != "?":
            return  # כבר נחשף
        
        btn["text"] = str(self.values[index])
        btn.update()
        
        if not self.first:
            self.first = index
        elif not self.second and index != self.first:
            self.second = index
            self.lock = True
            self.root.after(1000, self.check_match)

    def check_match(self):
        first_btn = self.buttons[self.first]
        second_btn = self.buttons[self.second]

        if self.values[self.first] == self.values[self.second]:
            self.matches += 1
            # לבדוק אם ניצחת
            if self.matches == 8:
                self.show_win_message()
        else:
            first_btn["text"] = "?"
            second_btn["text"] = "?"

        self.first = None
        self.second = None
        self.lock = False

    def show_win_message(self):
        win_label = tk.Label(self.root, text="כל הכבוד! ניצחת!", font=("Arial", 24), fg="green")
        win_label.grid(row=4, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
