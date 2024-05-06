from tkinter import *
from Params import *
from Tank import *
import random


def exit_game():
    screen.destroy()
def restart_game():
    pass

def on_key_press(event):
    if event.keysym == 'Left':
        Dysha.move_left()
    elif event.keysym == 'Right':
        Dysha.move_right()
    elif event.keysym == 'Up':
        Dysha.move_up()
    elif event.keysym == 'Down':
        Dysha.move_down()

def move_randomly():
    directions = ['Up', 'Down', 'Left', 'Right']
    direction = random.choice(directions)
    if direction == 'Up' and Enemy_Dysha.y > 0:
        Enemy_Dysha.move_up()
    elif direction == 'Down' and Enemy_Dysha.y < board_height - Enemy_Dysha.size:
        Enemy_Dysha.move_down()
    elif direction == 'Left' and Enemy_Dysha.x > 0:
        Enemy_Dysha.move_left()
    elif direction == 'Right' and Enemy_Dysha.x < board_width - Enemy_Dysha.size:
        Enemy_Dysha.move_right()

    screen.after(1000, move_randomly)


#work_with_screen
screen = Tk()
screen.attributes('-fullscreen', True)

canvas = Canvas(screen, bg=screen_color)
playing_board = canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                        outline=outline_color, width=outline_width, fill=board_color)
canvas.pack(fill=BOTH, expand=True)

exit_button = Button(screen, text="Вихід", command=exit_game, bg=botton_color,
                     width=12, height=4)
exit_button.place(x=20, y=20)
restart_button = Button(screen, text="Перезапустити гру", command=restart_game, bg=botton_color,
                     width=16, height=4)
restart_button.place(x=20, y=120)


if __name__ == '__main__':
    Dysha = Tank(canvas,220,125,50,"blue")
    Dysha.draw_tank()
    Enemy_Dysha = Tank(canvas,1075, 600,50,"red")
    Enemy_Dysha.draw_tank()

screen.bind('<KeyPress>', on_key_press)

move_randomly()
screen.mainloop()