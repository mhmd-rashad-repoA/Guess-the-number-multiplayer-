import tkinter as tk
from tkinter import messagebox
import random

# ----- Game Configs -----
DIFFICULTY_SETTINGS = {
    "Easy": {"range": 10, "time": 30},
    "Medium": {"range": 50, "time": 45},
    "Hard": {"range": 100, "time": 60}
}

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Number Guessing Game - Multiplayer")
        self.master.geometry("450x500")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f4f8")

        self.players = ["Player 1", "Player 2"]
        self.scores = {"Player 1": 0, "Player 2": 0}
        self.current_player = 0

        self.target_number = 0
        self.time_left = 0
        self.difficulty = tk.StringVar(value="Easy")
        self.timer_running = False

        self.setup_widgets()

    def setup_widgets(self):
        self.title_label = tk.Label(self.master, text="🎯 Number Guessing Game (Multiplayer)",
                                    font=("Helvetica", 16, "bold"), bg="#f0f4f8")
        self.title_label.pack(pady=15)

        tk.Label(self.master, text="Select Difficulty:", bg="#f0f4f8").pack()
        tk.OptionMenu(self.master, self.difficulty, *DIFFICULTY_SETTINGS.keys()).pack(pady=5)

        self.player_label = tk.Label(self.master, text=f"Current Turn: {self.players[self.current_player]}",
                                     font=("Helvetica", 12), bg="#f0f4f8")
        self.player_label.pack(pady=5)

        self.entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        self.submit_btn = tk.Button(self.master, text="Submit Guess", command=self.check_guess, bg="#4caf50",
                                    fg="white", font=("Helvetica", 12), width=20)
        self.submit_btn.pack(pady=5)

        self.start_btn = tk.Button(self.master, text="Start Game", command=self.start_game, bg="#2196f3",
                                   fg="white", font=("Helvetica", 12), width=20)
        self.start_btn.pack(pady=5)

        self.restart_btn = tk.Button(self.master, text="Restart Game", command=self.start_game, bg="#ff9800",
                                     fg="white", font=("Helvetica", 12), width=20)

        self.feedback_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg="#f0f4f8", fg="#333")
        self.feedback_label.pack(pady=10)

        self.timer_label = tk.Label(self.master, text="Time Left: 0s", font=("Helvetica", 14), bg="#f0f4f8", fg="#d32f2f")
        self.timer_label.pack(pady=5)

        self.score_label = tk.Label(self.master, text=self.get_score_text(), font=("Helvetica", 12), bg="#f0f4f8")
        self.score_label.pack(pady=5)

    def start_game(self):
        self.feedback_label.config(text="", fg="#333")
        self.entry.delete(0, tk.END)
        settings = DIFFICULTY_SETTINGS[self.difficulty.get()]
        self.target_number = random.randint(1, settings["range"])
        self.time_left = settings["time"]
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.timer_running = True
        self.restart_btn.pack_forget()
        self.submit_btn.config(state="normal")
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.master.after(1000, self.update_timer)
        elif self.time_left == 0 and self.timer_running:
            self.feedback_label.config(text=f"⏰ Time's up! The number was {self.target_number}.", fg="#d32f2f")
            self.timer_running = False
            self.submit_btn.config(state="disabled")
            self.restart_btn.pack(pady=10)

    def check_guess(self):
        if not self.timer_running:
            messagebox.showinfo("Info", "Please start the game first!")
            return

        try:
            guess = int(self.entry.get())
            if guess == self.target_number:
                winner = self.players[self.current_player]
                self.feedback_label.config(text=f"🎉 {winner} guessed right!", fg="#388e3c")
                self.scores[winner] += 1
                self.timer_running = False
                self.submit_btn.config(state="disabled")
                self.score_label.config(text=self.get_score_text())
                self.restart_btn.pack(pady=10)
            elif guess < self.target_number:
                self.feedback_label.config(text="📉 Too low!", fg="#333")
                self.switch_turn()
            else:
                self.feedback_label.config(text="📈 Too high!", fg="#333")
                self.switch_turn()
        except ValueError:
            self.feedback_label.config(text="⚠️ Please enter a valid number!", fg="#e65100")

    def switch_turn(self):
        self.current_player = 1 - self.current_player
        self.player_label.config(text=f"Current Turn: {self.players[self.current_player]}")
        self.entry.delete(0, tk.END)

    def get_score_text(self):
        return f"Scores - Player 1: {self.scores['Player 1']} | Player 2: {self.scores['Player 2']}"

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()
