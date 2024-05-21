from tkinter import Canvas
from Params import *

class Tank:
    def __init__(self, coords, size, color):
        self.canvas = Canvas
        self.coords = coords
        self.size = size
        self.color = color
        self.tank_shape = self.create_square()
        self.enemy_tank_shape = self.create_enemy_square()

    def create_square(self):
        self.square = self.canvas.create_rectangle(tank_coords[0], tank_coords[1],
                                                   tank_coords[0] + tank_size, tank_coords[1] + tank_size,
                                                   fill=square_color)

    def create_enemy_square(self):
        self.enemy_square = self.canvas.create_rectangle(enemy_coords[0], enemy_coords[1],
                                                         enemy_coords[0] + tank_size, enemy_coords[1] + tank_size,
                                                         fill=enemy_color)
    def move(self, dx, dy):
        self.canvas.move(self.tank_shape, dx, dy)

    def get_coords(self):
        return self.canvas.coords(self.tank_shape)

    def get_enemy_coords(self):
        return self.canvas.coords(self.enemy_tank_shape)

