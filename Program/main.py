from Root import *
from tkinter import *
def start_game():
    player_name = player_name_entry.get()
    enemy_name = enemy_name_entry.get()
    start_window.destroy()
    screen = Tk()
    dysha = Dysha_of_Tanks(screen, player_name, enemy_name)
    screen.mainloop()

# Початкове вікно для введення імені гравця
start_window = Tk()
start_window.title("Dysha of Tanks")

Label(start_window, text="Ім'я гравця:").pack()
player_name_entry = Entry(start_window)
player_name_entry.pack()

Label(start_window, text="Ім'я ворога:").pack()
enemy_name_entry = Entry(start_window)
enemy_name_entry.pack()

Button(start_window, text="Почати гру", command=start_game).pack()

start_window.mainloop()