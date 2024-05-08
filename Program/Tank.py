class Tank:
    def __init__(self, canvas, x, y, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = 5

    def draw_tank(self):
        self.obj = self.canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.color)

    def move_left(self):
        self.x -= self.speed
        self.canvas.move(self.obj, -self.speed, 0)

    def move_right(self):
        self.x += self.speed
        self.canvas.move(self.obj, self.speed, 0)

    def move_up(self):
        self.y -= self.speed
        self.canvas.move(self.obj, 0, -self.speed)

    def move_down(self):
        self.y += self.speed
        self.canvas.move(self.obj, 0, self.speed)


