import tkinter as tk
from tkinter import messagebox
import random
import time
import winsound
import threading
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MultiplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математический тренажер")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#004d00")

        self.user_name = ""
        self.difficulty = tk.StringVar(value="Средний")
        self.questions_count = 10
        self.time_limit = 60
        self.questions = []
        self.current_q = None
        self.solved_count = 0
        self.game_over = False
        
        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_sound(self, file_name):
        path = resource_path(file_name)
        try:
            threading.Thread(target=winsound.PlaySound, args=(path, winsound.SND_FILENAME), daemon=True).start()
        except:
            pass

    def show_author(self):
        # Окно с информацией о тебе
        messagebox.showinfo("Об авторе", "Программа: Математический тренажер\nРазработчик: Илья Катаев\n\nПроект создан для проверки знаний таблицы умножения.")

    def exit_app(self):
        self.root.destroy()

    def main_menu(self):
        self.game_over = False
        self.clear_screen()
        
        tk.Label(self.root, text="МАТЕМАТИЧЕСКИЙ ТРЕНАЖЕР", 
                 font=("Arial", 35, "bold"), bg="#004d00", fg="white").pack(pady=30)
        
        main_frame = tk.Frame(self.root, bg="#004d00")
        main_frame.pack(expand=True)

        label_style = {"bg": "#004d00", "fg": "white", "font": ("Arial", 16)}
        
        tk.Label(main_frame, text="Ваше имя:", **label_style).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.name_entry = tk.Entry(main_frame, font=("Arial", 18), width=15)
        self.name_entry.grid(row=0, column=1, pady=10)
        self.name_entry.focus()

        tk.Label(main_frame, text="Время (сек):", **label_style).grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.time_entry = tk.Entry(main_frame, font=("Arial", 18), width=15)
        self.time_entry.grid(row=1, column=1, pady=10)
        self.time_entry.insert(0, "60")

        tk.Label(main_frame, text="Кол-во примеров:", **label_style).grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.count_entry = tk.Entry(main_frame, font=("Arial", 18), width=15)
        self.count_entry.grid(row=2, column=1, pady=10)
        self.count_entry.insert(0, "10")

        tk.Label(main_frame, text="Сложность:", bg="#004d00", fg="yellow", font=("Arial", 18, "bold")).grid(row=3, column=0, columnspan=2, pady=20)
        levels_frame = tk.Frame(main_frame, bg="#004d00")
        levels_frame.grid(row=4, column=0, columnspan=2)
        
        for lvl in ["Легкий", "Средний", "Сложный"]:
            tk.Radiobutton(levels_frame, text=lvl, variable=self.difficulty, value=lvl, 
                           bg="#004d00", fg="white", selectcolor="black", font=("Arial", 14)).pack(side="left", padx=15)

        tk.Button(self.root, text="НАЧАТЬ ТЕСТ", command=self.start_training, 
                  bg="#4CAF50", fg="white", font=("Arial", 22, "bold"), padx=50, pady=15).pack(pady=10)
        
        # Блок кнопок в самом низу
        bottom_frame = tk.Frame(self.root, bg="#004d00")
        bottom_frame.pack(side="bottom", pady=30)

        tk.Button(bottom_frame, text="ОБ АВТОРЕ", command=self.show_author, 
                  bg="#34495e", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=20)
        
        tk.Button(bottom_frame, text="ВЫХОД", command=self.exit_app, 
                  bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=20)

    # ... (остальные функции start_training, next_question, game_screen, check_answer, update_timer_display остаются такими же)

    def start_training(self):
        self.user_name = self.name_entry.get() if self.name_entry.get() else "Ученик"
        try:
            self.time_limit = int(self.time_entry.get())
            self.questions_count = int(self.count_entry.get())
        except:
            messagebox.showerror("Ошибка", "Введите числа!")
            return
        diff = self.difficulty.get()
        r = range(1, 6) if diff == "Легкий" else range(2, 21) if diff == "Сложный" else range(1, 11)
        all_pairs = [(a, b) for a in r for b in r]
        random.shuffle(all_pairs)
        self.questions = all_pairs[:self.questions_count]
        self.solved_count = 0
        self.game_over = False
        self.start_time = time.time()
        self.next_question()

    def next_question(self):
        if self.game_over: return
        if not self.questions:
            self.finish_game(success=True)
            return
        self.current_q = self.questions.pop()
        self.game_screen()

    def game_screen(self):
        self.clear_screen()
        info_frame = tk.Frame(self.root, bg="#004d00")
        info_frame.pack(fill="x", padx=50, pady=20)
        tk.Label(info_frame, text=f"Игрок: {self.user_name}", font=("Arial", 18), bg="#004d00", fg="white").pack(side="left")
        tk.Label(info_frame, text=f"Решено: {self.solved_count} / {self.questions_count}", font=("Arial", 18), bg="#004d00", fg="white").pack(side="right")
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 25, "bold"), fg="#ffcc00", bg="#004d00")
        self.timer_label.pack(pady=10)
        self.update_timer_display()
        self.label_q = tk.Label(self.root, text=f"{self.current_q[0]} × {self.current_q[1]} =", font=("Arial", 80, "bold"), bg="#004d00", fg="white")
        self.label_q.pack(expand=True)
        self.answer_entry = tk.Entry(self.root, font=("Arial", 50), width=6, justify='center')
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        self.answer_entry.focus()
        tk.Button(self.root, text="ПРОВЕРИТЬ", command=self.check_answer, bg="#2196F3", fg="white", font=("Arial", 22, "bold"), padx=40, pady=10).pack(pady=40)

    def check_answer(self):
        if self.game_over: return
        try:
            val = int(self.answer_entry.get())
            if val == self.current_q[0] * self.current_q[1]:
                self.play_sound("win.wav") 
                self.solved_count += 1
                self.next_question()
            else:
                self.play_sound("lose.wav") 
                self.answer_entry.delete(0, tk.END)
        except:
            self.answer_entry.delete(0, tk.END)

    def update_timer_display(self):
        if self.game_over: return
        rem = int(self.time_limit - (time.time() - self.start_time))
        if rem <= 0: self.finish_game(success=False)
        else:
            if hasattr(self, 'timer_label'):
                self.timer_label.config(text=f"⏱ ОСТАЛОСЬ: {rem} сек")
                self.root.after(1000, self.update_timer_display)

    def finish_game(self, success):
        self.game_over = True
        self.clear_screen()
        if success:
            self.play_sound("win.wav")
            txt, color = "ПОЗДРАВЛЯЕМ! 🎉", "#4CAF50"
        else:
            self.play_sound("lose.wav")
            txt, color = "ВРЕМЯ ИСТЕКЛО! ⏰", "#ff4d4d"
        tk.Label(self.root, text=txt, font=("Arial", 50, "bold"), fg=color, bg="#004d00").pack(expand=True)
        tk.Label(self.root, text=f"{self.user_name}, твой результат: {self.solved_count} из {self.questions_count}", font=("Arial", 22), fg="white", bg="#004d00").pack(expand=True)
        tk.Button(self.root, text="В ГЛАВНОЕ МЕНЮ", command=self.main_menu, bg="#9E9E9E", fg="white", font=("Arial", 18, "bold"), padx=40, pady=15).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiplicationApp(root)
    root.mainloop()