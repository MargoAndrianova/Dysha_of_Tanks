from tkinter import *
from Params import *

class Dysha_of_Tanks:
    def __init__(self, screen):
        self.screen = screen
        self.screen.attributes('-fullscreen', True)

        self.canvas = Canvas(self.screen, bg=screen_color)
        self.canvas.pack(fill=BOTH, expand=True)

        self.playing_board = self.canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                                          outline=outline_color, width=2, fill=board_color)

        self.exit_button = Button(self.screen, text="Вихід", command=self.exit_game, bg=botton_color,
                             width=12, height=4)
        self.exit_button.place(x=20, y=20)

        self.step_size = step_of_tank
        self.square_size = tank_size

        self.screen.bind('<Escape>', lambda event: self.screen.quit())
        self.screen.bind('<Key>', self.move_square)

    def move_square(self, event):
        key = event.keysym
        if key == 'Up':
            self.canvas.move(self.square, 0, -self.step_size)
        elif key == 'Down':
            self.canvas.move(self.square, 0, self.step_size)
        elif key == 'Left':
            self.canvas.move(self.square, -self.step_size, 0)
        elif key == 'Right':
            self.canvas.move(self.square, self.step_size, 0)


        x1, y1, x2, y2 = self.canvas.coords(self.square)
        if x1 < edge_distance_width:
            self.canvas.move(self.square, edge_distance_width - x1, 0)
        if y1 < edge_distance_height:
            self.canvas.move(self.square, 0, edge_distance_height - y1)
        if x2 > board_width:
            self.canvas.move(self.square, board_width - x2, 0)
        if y2 > board_height:
            self.canvas.move(self.square, 0, board_height - y2)

    def create_square(self):
        self.square = self.canvas.create_rectangle(600, 400, 625, 425, fill=square_color)

    def exit_game(self):
        self.screen.destroy()

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    dysha.create_square()
    screen.mainloop()