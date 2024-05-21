from tkinter import Canvas


class Bullet:
    def __init__(self, canvas, start_pos, color):
        self.canvas = canvas
        self.color = color
        x, y = start_pos
        self.bullet_shape = self.canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill=color)

    def move(self):
        self.canvas.move(self.bullet_shape, 0, -10)  # беремо bullet_speed з params, якщо потрібно

    def get_coords(self):
        return self.canvas.coords(self.bullet_shape)

    def destroy(self):
        self.canvas.delete(self.bullet_shape)

