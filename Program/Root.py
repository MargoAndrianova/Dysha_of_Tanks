from tkinter import *
from Params import *
import time
import math

class Dysha_of_Tanks:
    def __init__(self, screen):
        self.screen = screen
        self.screen.attributes('-fullscreen', True)

        self.canvas = Canvas(self.screen, bg=screen_color)
        self.canvas.pack(fill=BOTH, expand=True)

        self.playing_board = self.canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                                          outline=outline_color, width=outline_width, fill=board_color)

        self.exit_button = Button(self.screen, text="Вихід", command=self.exit_game, bg=botton_color,
                                  width=12, height=4)
        self.exit_button.place(x=20, y=20)

        self.step_size = step_of_tank
        self.square_size = tank_size

        self.keys_pressed = set()
        self.bullets = []
        self.enemy_bullets = []

        self.last_shot_time_player = 0
        self.last_shot_time_enemy = 0

        self.player_angle = 180  # Кут повороту танка гравця в градусах
        self.enemy_angle = 0   # Кут повороту ворожого танка в градусах

        self.screen.bind('<Escape>', lambda event: self.screen.quit())
        self.screen.bind('<KeyPress>', self.handle_key_press)
        self.screen.bind('<KeyRelease>', self.handle_key_release)

        self.create_square()
        self.create_enemy_square()

        self.move_bullets()
        self.move_enemy_bullets()
        self.check_bullet_collision()
        self.update_movement()

    def create_square(self):
        x, y = tank_coords
        self.square = self.create_rotated_polygon(x, y, self.square_size, self.player_angle, square_color)

    def create_enemy_square(self):
        x, y = enemy_coords
        self.enemy_square = self.create_rotated_polygon(x, y, self.square_size, self.enemy_angle, enemy_color)

    def create_rotated_polygon(self, x, y, size, angle, color):
        points = self.calculate_square_points(x, y, size, angle)
        return self.canvas.create_polygon(points, fill=color)

    def calculate_square_points(self, x, y, size, angle):
        half_size = size / 2
        rad = math.radians(angle)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)

        points = [
            (x + half_size * cos_val - half_size * sin_val, y + half_size * sin_val + half_size * cos_val),
            (x - half_size * cos_val - half_size * sin_val, y - half_size * sin_val + half_size * cos_val),
            (x - half_size * cos_val + half_size * sin_val, y - half_size * sin_val - half_size * cos_val),
            (x + half_size * cos_val + half_size * sin_val, y + half_size * sin_val - half_size * cos_val)
        ]

        return points

    def handle_key_press(self, event):
        key = event.keysym
        self.keys_pressed.add(key)
        if key.lower() == 'shift_l':
            self.shoot(self.square, self.player_angle + 180)  # Стріляє в протилежну сторону
        if key.lower() == 'shift_r':
            self.shoot_enemy(self.enemy_square, self.enemy_angle + 180)  # Стріляє з протилежної сторони танка

    def handle_key_release(self, event):
        key = event.keysym
        self.keys_pressed.discard(key)

    def update_movement(self):
        for key in self.keys_pressed:
            if key.lower() == 'w':
                self.move_tank(self.square, self.player_angle, -self.step_size)
            if key.lower() == 's':
                self.move_tank(self.square, self.player_angle, self.step_size)
            if key == 'Up':
                self.move_tank(self.enemy_square, self.enemy_angle, -self.step_size)
            if key == 'Down':
                self.move_tank(self.enemy_square, self.enemy_angle, self.step_size)
            if key.lower() == 'a':
                self.player_angle -= 5  # Поворот вліво
                self.update_tank_rotation(self.square, self.player_angle)
            if key.lower() == 'd':
                self.player_angle += 5  # Поворот вправо
                self.update_tank_rotation(self.square, self.player_angle)
            if key == 'Left':
                self.enemy_angle -= 5  # Поворот вліво
                self.update_tank_rotation(self.enemy_square, self.enemy_angle)
            if key == 'Right':
                self.enemy_angle += 5  # Поворот вправо
                self.update_tank_rotation(self.enemy_square, self.enemy_angle)

        self.limit_movement(self.square)
        self.limit_movement(self.enemy_square)

        self.screen.after(50, self.update_movement)

    def move_tank(self, tank, angle, step):
        rad = math.radians(angle)
        dx = step * math.cos(rad)
        dy = step * math.sin(rad)
        self.canvas.move(tank, dx, dy)

    def update_tank_rotation(self, tank, angle):
        x, y = self.get_tank_center(tank)
        points = self.calculate_square_points(x, y, self.square_size, angle)
        self.canvas.coords(tank, *sum(points, ()))

    def get_tank_center(self, tank):
        coords = self.canvas.coords(tank)
        x = sum(coords[::2]) / len(coords[::2])
        y = sum(coords[1::2]) / len(coords[1::2])
        return x, y

    def limit_movement(self, object):
        # Обмеження для танка
        coords = self.canvas.coords(object)
        x1, y1, x2, y2 = min(coords[::2]), min(coords[1::2]), max(coords[::2]), max(coords[1::2])
        if x1 <= edge_distance_width:
            self.canvas.move(object, edge_distance_width - x1, 0)
        if y1 <= edge_distance_height:
            self.canvas.move(object, 0, edge_distance_height - y1)
        if x2 >= board_width:
            self.canvas.move(object, board_width - x2, 0)
        if y2 >= board_height:
            self.canvas.move(object, 0, board_height - y2)

    def limit_bullet(self, object):
        x1, y1, x2, y2 = self.canvas.coords(object)
        if x1 <= edge_distance_width - outline_width or x2 >= board_width - outline_width or y1 <= edge_distance_height - outline_width or y2 >= board_height - outline_width:
            self.canvas.delete(object)
            if object in [bullet[0] for bullet in self.bullets]:
                self.bullets = [bullet for bullet in self.bullets if bullet[0] != object]
            else:
                self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet[0] != object]

    def shoot(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_player >= 1:
            bullet_coords = self.calculate_bullet_coords(tank, angle)
            bullet = self.canvas.create_rectangle(bullet_coords, fill=bullet_color)
            self.bullets.append((bullet, angle))  # Зберігаємо кут разом з кулею
            self.last_shot_time_player = current_time

    def shoot_enemy(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_enemy >= 1:
            bullet_coords = self.calculate_bullet_coords(tank, angle)
            bullet = self.canvas.create_rectangle(bullet_coords, fill=enemy_bullet_color)
            self.enemy_bullets.append((bullet, angle))  # Зберігаємо кут разом з кулею
            self.last_shot_time_enemy = current_time

    def calculate_bullet_coords(self, tank, angle):
        x, y = self.get_tank_front(tank, angle)
        return x - 2, y - 2, x + 2, y + 2

    def get_tank_front(self, tank, angle):
        x, y = self.get_tank_center(tank)
        rad = math.radians(angle)
        front_x = x + (tank_size / 2) * math.cos(rad)
        front_y = y + (tank_size / 2) * math.sin(rad)
        return front_x, front_y

    def move_bullets(self):
        for bullet, angle in self.bullets[:]:
            self.move_bullet(bullet, angle)
        self.screen.after(bullet_interval, self.move_bullets)

    def move_enemy_bullets(self):
        for bullet, angle in self.enemy_bullets[:]:
            self.move_bullet(bullet, angle)
        self.screen.after(bullet_interval, self.move_enemy_bullets)

    def move_bullet(self, bullet, angle):
        rad = math.radians(angle)
        dx = bullet_speed * math.cos(rad)
        dy = bullet_speed * math.sin(rad)
        self.canvas.move(bullet, dx, dy)
        self.limit_bullet(bullet)

    def check_bullet_collision(self):
        # Перевірка попадання куль гравця у ворожий танк
        for bullet, _ in self.bullets[:]:
            if self.check_collision(bullet, self.enemy_square):
                self.canvas.delete(bullet)
                self.bullets.remove((bullet, _))

        # Перевірка попадання куль ворога у танк гравця
        for bullet, _ in self.enemy_bullets[:]:
            if self.check_collision(bullet, self.square):
                self.canvas.delete(bullet)
                self.enemy_bullets.remove((bullet, _))

        self.screen.after(bullet_interval, self.check_bullet_collision)

    def check_collision(self, bullet, tank):
        bullet_coords = self.canvas.coords(bullet)
        tank_coords = self.canvas.coords(tank)
        bullet_x1, bullet_y1, bullet_x2, bullet_y2 = min(bullet_coords[::2]), min(bullet_coords[1::2]), max(bullet_coords[::2]), max(bullet_coords[1::2])
        tank_x1, tank_y1, tank_x2, tank_y2 = min(tank_coords[::2]), min(tank_coords[1::2]), max(tank_coords[::2]), max(tank_coords[1::2])
        return bullet_x1 < tank_x2 and bullet_x2 > tank_x1 and bullet_y1 < tank_y2 and bullet_y2 > tank_y1

    def exit_game(self):
        self.screen.destroy()

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    screen.mainloop()