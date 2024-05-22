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

        self.exit_button = Button(self.screen, text="Exit", command=self.exit_game, bg=botton_color,
                                  width=12, height=4)
        self.exit_button.place(x=20, y=20)

        self.step_size = step_of_tank
        self.square_size = tank_size

        self.keys_pressed = set()
        self.bullets = []
        self.enemy_bullets = []

        self.last_shot_time_player = 0
        self.last_shot_time_enemy = 0

        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.damage = damage  # HP reduction on hit
        self.touch_damage = touch_damage  # HP reduction on collision

        self.hp_length = hp_length
        self.hp_height = hp_height
        self.hp_outline_width = hp_outline_width

        # Placing HP bars
        self.player_hp_bar = self.canvas.create_rectangle(edge_distance_width, edge_distance_height - self.hp_height - 10,
                                                          edge_distance_width + self.hp_length, edge_distance_height - 10,
                                                          outline='black', width=self.hp_outline_width)
        self.player_hp_fill = self.canvas.create_rectangle(edge_distance_width, edge_distance_height - self.hp_height - 10,
                                                           edge_distance_width + self.hp_length, edge_distance_height - 10,
                                                           fill='red')

        self.enemy_hp_bar = self.canvas.create_rectangle(board_width - self.hp_length, board_height + 20,
                                                         board_width, board_height + self.hp_height + 20,
                                                         outline='black', width=self.hp_outline_width)
        self.enemy_hp_fill = self.canvas.create_rectangle(board_width - self.hp_length, board_height + 20,
                                                          board_width, board_height + self.hp_height + 20,
                                                          fill='red')

        self.player_hp_text = self.canvas.create_text(edge_distance_width + self.hp_length + 40, edge_distance_height - self.hp_height / 2 - 10,
                                                      text=f'HP: {self.player_hp}', font=('Arial', 14), fill='black')
        self.enemy_hp_text = self.canvas.create_text(board_width - self.hp_length - 50, board_height + 20 + self.hp_height / 2,
                                                     text=f'HP: {self.enemy_hp}', font=('Arial', 14), fill='black')

        self.player_angle = player_angle  # Initial player tank angle
        self.enemy_angle = enemy_angle  # Initial enemy tank angle

        self.screen.bind('<Escape>', lambda event: self.screen.quit())
        self.screen.bind('<KeyPress>', self.handle_key_press)
        self.screen.bind('<KeyRelease>', self.handle_key_release)

        # Disable Caps Lock and Tab keys
        self.screen.bind('<Caps_Lock>', self.disable_key)
        self.screen.bind('<Tab>', self.disable_key)

        self.create_square()
        self.create_enemy_square()

        self.move_bullets()
        self.move_enemy_bullets()
        self.check_bullet_collision()
        self.update_movement()
        self.check_tank_collision()

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
            self.shoot(self.square, self.player_angle + 180)  # Shoot in the opposite direction
        if key.lower() == 'shift_r':
            self.shoot_enemy(self.enemy_square, self.enemy_angle + 180)  # Shoot in the opposite direction

    def handle_key_release(self, event):
        key = event.keysym
        self.keys_pressed.discard(key)

    def disable_key(self, event):
        return "break"

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
                self.player_angle -= angle_turn  # Turn left
                self.update_tank_rotation(self.square, self.player_angle)
            if key.lower() == 'd':
                self.player_angle += angle_turn  # Turn right
                self.update_tank_rotation(self.square, self.player_angle)
            if key == 'Left':
                self.enemy_angle -= angle_turn  # Turn left
                self.update_tank_rotation(self.enemy_square, self.enemy_angle)
            if key == 'Right':
                self.enemy_angle += angle_turn  # Turn right
                self.update_tank_rotation(self.enemy_square, self.enemy_angle)

        self.limit_movement(self.square)
        self.limit_movement(self.enemy_square)

        self.screen.after(50, self.update_movement)

    def move_tank(self, tank, angle, step):
        rad = math.radians(angle)
        dx = step * math.cos(rad)
        dy = step * math.sin(rad)
        self.canvas.move(tank, dx, dy)
        self.prevent_tank_overlap()

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
            self.bullets.append((bullet, angle))
            self.last_shot_time_player = current_time

    def shoot_enemy(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_enemy >= 1:
            bullet_coords = self.calculate_bullet_coords(tank, angle)
            bullet = self.canvas.create_rectangle(bullet_coords, fill=enemy_bullet_color)
            self.enemy_bullets.append((bullet, angle))
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
        for bullet, _ in self.bullets[:]:
            if self.check_collision(bullet, self.enemy_square):
                self.canvas.delete(bullet)
                self.bullets.remove((bullet, _))
                self.enemy_hp -= self.damage
                self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)

        for bullet, _ in self.enemy_bullets[:]:
            if self.check_collision(bullet, self.square):
                self.canvas.delete(bullet)
                self.enemy_bullets.remove((bullet, _))
                self.player_hp -= self.damage
                self.update_hp_bar(self.player_hp_fill, self.player_hp, self.player_hp_text)

        self.screen.after(bullet_interval, self.check_bullet_collision)

    def check_collision(self, bullet, tank):
        bullet_coords = self.canvas.coords(bullet)
        tank_coords = self.canvas.coords(tank)
        bullet_x1, bullet_y1, bullet_x2, bullet_y2 = min(bullet_coords[::2]), min(bullet_coords[1::2]), max(bullet_coords[::2]), max(bullet_coords[1::2])
        tank_x1, tank_y1, tank_x2, tank_y2 = min(tank_coords[::2]), min(tank_coords[1::2]), max(tank_coords[::2]), max(tank_coords[1::2])
        return bullet_x1 < tank_x2 and bullet_x2 > tank_x1 and bullet_y1 < tank_y2 and bullet_y2 > tank_y1

    def check_tank_collision(self):
        if self.tanks_collide():
            self.player_hp -= self.touch_damage
            self.enemy_hp -= self.touch_damage
            self.update_hp_bar(self.player_hp_fill, self.player_hp, self.player_hp_text)
            self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)
            self.reset_tanks()
        self.screen.after(100, self.check_tank_collision)

    def tanks_collide(self):
        player_coords = self.canvas.coords(self.square)
        enemy_coords = self.canvas.coords(self.enemy_square)
        player_x1, player_y1, player_x2, player_y2 = min(player_coords[::2]), min(player_coords[1::2]), max(player_coords[::2]), max(player_coords[1::2])
        enemy_x1, enemy_y1, enemy_x2, enemy_y2 = min(enemy_coords[::2]), min(enemy_coords[1::2]), max(enemy_coords[::2]), max(enemy_coords[1::2])
        return player_x1 < enemy_x2 and player_x2 > enemy_x1 and player_y1 < enemy_y2 and player_y2 > enemy_y1

    def reset_tanks(self):
        self.player_hp = max(self.player_hp - self.touch_damage, 0)
        self.enemy_hp = max(self.enemy_hp - self.touch_damage, 0)
        self.update_hp_bar(self.player_hp_fill, self.player_hp, self.player_hp_text)
        self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)
        self.canvas.coords(self.square, *sum(self.calculate_square_points(*tank_coords, self.square_size, self.player_angle), ()))
        self.canvas.coords(self.enemy_square, *sum(self.calculate_square_points(*enemy_coords, self.square_size, self.enemy_angle), ()))

    def prevent_tank_overlap(self):
        if self.tanks_collide():
            self.reset_tanks()

    def update_hp_bar(self, fill, hp, text):
        hp = max(hp, 0)  # Ensure HP doesn't go below 0
        bar_length = self.hp_length * hp / 100  # Proportional HP bar length
        self.canvas.coords(fill, self.canvas.coords(fill)[0], self.canvas.coords(fill)[1],
                           self.canvas.coords(fill)[0] + bar_length, self.canvas.coords(fill)[3])
        self.canvas.itemconfig(text, text=f'HP: {hp}')
        if hp <= 0:
            self.game_over()

    def game_over(self):
        winner = "Player" if self.enemy_hp <= 0 else "Enemy"
        self.canvas.create_text(board_width // 2, board_height // 2, text=f"{winner} Wins!", font=("Arial", 50), fill="red")
        self.screen.after(2000, self.exit_game)  # Delay before exit

    def exit_game(self):
        self.screen.destroy()

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    screen.mainloop()
