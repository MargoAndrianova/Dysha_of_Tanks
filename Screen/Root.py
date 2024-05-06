from tkinter import *
from Params import *

def exit_game():
    screen.destroy()

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

screen.mainloop()