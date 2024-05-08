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
        self.screen.bind('<Key>', self.handle_key_event)
        self.screen.bind('<KeyRelease>', self.handle_key_release)
        self.keys_pressed = set()

    def handle_key_event(self, event):
        key = event.keysym
        self.keys_pressed.add(key)
        self.move_square()
        self.move_enemy_square()

    def handle_key_release(self, event):
        key = event.keysym
        self.keys_pressed.remove(key)

    def move_square(self):
        if 'Up' in self.keys_pressed:
            self.canvas.move(self.square, 0, -self.step_size)
        if 'Down' in self.keys_pressed:
            self.canvas.move(self.square, 0, self.step_size)
        if 'Left' in self.keys_pressed:
            self.canvas.move(self.square, -self.step_size, 0)
        if 'Right' in self.keys_pressed:
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

    def move_enemy_square(self):
        if 'w' in self.keys_pressed:
            self.canvas.move(self.enemy_square, 0, -self.step_size)
        if 's' in self.keys_pressed:
            self.canvas.move(self.enemy_square, 0, self.step_size)
        if 'a' in self.keys_pressed:
            self.canvas.move(self.enemy_square, -self.step_size, 0)
        if 'd' in self.keys_pressed:
            self.canvas.move(self.enemy_square, self.step_size, 0)

        x1, y1, x2, y2 = self.canvas.coords(self.enemy_square)
        if x1 < edge_distance_width:
            self.canvas.move(self.enemy_square, edge_distance_width - x1, 0)
        if y1 < edge_distance_height:
            self.canvas.move(self.enemy_square, 0, edge_distance_height - y1)
        if x2 > board_width:
            self.canvas.move(self.enemy_square, board_width - x2, 0)
        if y2 > board_height:
            self.canvas.move(self.enemy_square, 0, board_height - y2)

    def exit_game(self):
        self.screen.destroy()

    def create_square(self):
        self.square = self.canvas.create_rectangle(tank_coords[0], tank_coords[1],
                                                   tank_coords[0]+tank_size, tank_coords[1]+tank_size,
                                                   fill=square_color)
    def create_enemy_square(self):
        self.enemy_square = self.canvas.create_rectangle(enemy_coords[0], enemy_coords[1],
                                                         enemy_coords[0] + tank_size, enemy_coords[1] + tank_size,
                                                         fill=enemy_color)

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    dysha.create_square()
    dysha.create_enemy_square()
    screen.mainloop()