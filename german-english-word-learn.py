import tkinter as tk
from tkinter import Entry, Label, messagebox
import json
import random

class GermanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("German Learning App")

        # Load existing data from JSON file
        self.data = self.load_data()

        # Create GUI components
        self.label = Label(root, text="", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.play_button = tk.Button(root, text="Play", command=self.play_word)
        self.play_button.pack(pady=10)

        self.answer_entry = Entry(root)
        self.answer_entry.pack(pady=10)

        self.check_button = tk.Button(root, text="Check", command=self.check_answer)
        self.check_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", command=self.next_word, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Add", command=self.show_add_dialog)
        self.next_button.pack(pady=10)

    def load_data(self):
        try:
            with open("german_words.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def save_data(self):
        with open("german_words.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    def play_word(self):
        if not self.data:
            self.label.config(text="No words available. Add some first!")
            return

        self.current_german_word = random.choice(list(self.data.keys()))
        self.label.config(text=self.current_german_word)
        self.play_button.config(state=tk.DISABLED)
        self.answer_entry.config(state=tk.NORMAL)
        self.check_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.data.get(self.current_german_word, "").lower()

        if user_answer == correct_answer:
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", "Your answer is incorrect. Try again.")

        self.play_button.config(state=tk.NORMAL)
        self.answer_entry.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_word(self):
        self.label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.play_button.config(state=tk.NORMAL)
        self.answer_entry.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

    def show_add_dialog(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Word")

        german_label = tk.Label(add_window, text="German Word:")
        german_label.pack()

        german_entry = Entry(add_window)
        german_entry.pack()

        english_label = tk.Label(add_window, text="English Translation:")
        english_label.pack()

        english_entry = Entry(add_window)
        english_entry.pack()

        add_button = tk.Button(
            add_window, text="Add Word", command=lambda: self.add_word(
                german_entry.get(), english_entry.get(), add_window)
        )
        add_button.pack()

    def add_word(self, german, english, add_window):
        if german and english:
            self.data[german] = english
            self.save_data()
            add_window.destroy()
        else:
            tk.messagebox.showwarning("Error", "Both fields must be filled!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GermanApp(root)
    root.mainloop()
