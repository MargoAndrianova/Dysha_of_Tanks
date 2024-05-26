from tkinter import *
from Params import *
import time
import math
import random

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
        self.original_step_size = step_of_tank
        self.square_size = tank_size

        self.keys_pressed = {
            'w': False,
            's': False,
            'a': False,
            'd': False,
            'Up': False,
            'Down': False,
            'Left': False,
            'Right': False
        }
        self.bullets = []
        self.enemy_bullets = []
        self.boosts = []
        self.bushes = []

        self.last_shot_time_player = 0
        self.last_shot_time_enemy = 0
        self.player_speed_boost_time = 0
        self.enemy_speed_boost_time = 0

        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.touch_damage = touch_damage  # Зменшення HP при зіткненні

        self.hp_length = hp_length
        self.hp_height = hp_height
        self.hp_outline_width = hp_outline_width

        self.bullet_speed = bullet_speed
        self.original_bullet_speed = bullet_speed
        self.player_bullet_speed_boost_time = 0
        self.enemy_bullet_speed_boost_time = 0

        # Розміщення шкал HP
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

        self.player_angle = player_angle  # Початковий кут повороту танка гравця
        self.enemy_angle = enemy_angle  # Кут повороту ворожого танка в градусах

        self.player_direction = {'x': 0, 'y': 0}
        self.enemy_direction = {'x': 0, 'y': 0}

        self.player_step_size = self.step_size
        self.enemy_step_size = self.step_size

        self.screen.bind('<Escape>', lambda event: self.screen.quit())
        self.screen.bind('<KeyPress>', self.handle_key_press)
        self.screen.bind('<KeyRelease>', self.handle_key_release)

        # Відключення клавіш Caps Lock та Tab
        self.screen.bind('<Caps_Lock>', self.disable_key)
        self.screen.bind('<Tab>', self.disable_key)

        self.create_square()
        self.create_enemy_square()

        self.spawn_bushes()
        self.move_bullets()
        self.move_enemy_bullets()
        self.check_bullet_collision()
        self.update_movement()
        self.check_tank_collision()
        self.update_damage_based_on_distance()
        self.spawn_boost()
        self.check_boost_collision()

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
        if key in self.keys_pressed:
            self.keys_pressed[key] = True
        if key.lower() == 'shift_l':
            self.shoot(self.square, self.player_angle + 180)  # Стріляє в протилежну сторону
        if key.lower() == 'shift_r':
            self.shoot_enemy(self.enemy_square, self.enemy_angle + 180)  # Стріляє з протилежної сторони танка

    def handle_key_release(self, event):
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed[key] = False

    def disable_key(self, event):
        return "break"

    def update_movement(self):
        self.update_player_direction()
        self.update_enemy_direction()

        self.move_tank(self.square, self.player_angle, self.player_direction, self.player_step_size)
        self.move_tank(self.enemy_square, self.enemy_angle, self.enemy_direction, self.enemy_step_size)

        self.screen.after(50, self.update_movement)

    def update_player_direction(self):
        self.player_direction = {'x': 0, 'y': 0}
        if self.keys_pressed['w']:
            self.player_direction['y'] = -self.player_step_size
        if self.keys_pressed['s']:
            self.player_direction['y'] = self.player_step_size
        if self.keys_pressed['a']:
            self.player_angle -= angle_turn  # Поворот вліво
            self.update_tank_rotation(self.square, self.player_angle)
        if self.keys_pressed['d']:
            self.player_angle += angle_turn  # Поворот вправо
            self.update_tank_rotation(self.square, self.player_angle)

    def update_enemy_direction(self):
        self.enemy_direction = {'x': 0, 'y': 0}
        if self.keys_pressed['Up']:
            self.enemy_direction['y'] = -self.enemy_step_size
        if self.keys_pressed['Down']:
            self.enemy_direction['y'] = self.enemy_step_size
        if self.keys_pressed['Left']:
            self.enemy_angle -= angle_turn  # Поворот вліво
            self.update_tank_rotation(self.enemy_square, self.enemy_angle)
        if self.keys_pressed['Right']:
            self.enemy_angle += angle_turn  # Поворот вправо
            self.update_tank_rotation(self.enemy_square, self.enemy_angle)

    def move_tank(self, tank, angle, direction, step_size):
        rad = math.radians(angle)
        dx = direction['y'] * math.cos(rad) - direction['x'] * math.sin(rad)
        dy = direction['y'] * math.sin(rad) + direction['x'] * math.cos(rad)

        self.canvas.move(tank, dx, dy)
        self.limit_movement(tank)
        self.prevent_tank_overlap()
        self.hide_tank_in_bush(tank)

    def update_tank_rotation(self, tank, angle):
        x, y = self.get_tank_center(tank)
        points = self.calculate_square_points(x, y, self.square_size, angle)
        self.canvas.coords(tank, *sum(points, ()))

    def get_tank_center(self, tank):
        coords = self.canvas.coords(tank)
        x = sum(coords[::2]) / len(coords[::2])
        y = sum(coords[1::2]) / len(coords[1::2])
        return x, y

    def limit_movement(self, tank):
        coords = self.canvas.coords(tank)
        x1, y1, x2, y2 = min(coords[::2]), min(coords[1::2]), max(coords[::2]), max(coords[1::2])
        if x1 < edge_distance_width:
            self.canvas.move(tank, edge_distance_width - x1, 0)
        if y1 < edge_distance_height:
            self.canvas.move(tank, 0, edge_distance_height - y1)
        if x2 > board_width:
            self.canvas.move(tank, board_width - x2, 0)
        if y2 > board_height:
            self.canvas.move(tank, 0, board_height - y2)

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
            self.show_tank(tank)  # Показати танк після стрільби
            self.screen.after(3000, lambda: self.hide_tank_in_bush(tank))  # Заховати танк через 3 секунди

    def shoot_enemy(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_enemy >= 1:
            bullet_coords = self.calculate_bullet_coords(tank, angle)
            bullet = self.canvas.create_rectangle(bullet_coords, fill=enemy_bullet_color)
            self.enemy_bullets.append((bullet, angle))
            self.last_shot_time_enemy = current_time
            self.show_tank(tank)  # Показати танк після стрільби
            self.screen.after(3000, lambda: self.hide_tank_in_bush(tank))  # Заховати танк через 3 секунди

    def shoot_in_all_directions(self, tank):
        directions = [0, 90, 180, 270]
        for angle in directions:
            bullet_coords = self.calculate_bullet_coords(tank, angle)
            bullet = self.canvas.create_rectangle(bullet_coords, fill=bullet_color)
            self.bullets.append((bullet, angle))

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
        dx = self.bullet_speed * math.cos(rad)
        dy = self.bullet_speed * math.sin(rad)
        self.canvas.move(bullet, dx, dy)
        self.limit_bullet(bullet)

    def check_bullet_collision(self):
        for bullet, _ in self.bullets[:]:
            if self.check_collision(bullet, self.enemy_square):
                self.canvas.delete(bullet)
                self.bullets.remove((bullet, _))
                self.enemy_hp -= self.get_damage()
                self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)

        for bullet, _ in self.enemy_bullets[:]:
            if self.check_collision(bullet, self.square):
                self.canvas.delete(bullet)
                self.enemy_bullets.remove((bullet, _))
                self.player_hp -= self.get_damage()
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
        hp = max(hp, 0)  # Забезпечуємо, що HP не стає меншим за 0
        bar_length = self.hp_length * hp / 100  # Пропорційна довжина шкали HP
        self.canvas.coords(fill, self.canvas.coords(fill)[0], self.canvas.coords(fill)[1],
                           self.canvas.coords(fill)[0] + bar_length, self.canvas.coords(fill)[3])
        self.canvas.itemconfig(text, text=f'HP: {hp}')
        if hp <= 0:
            self.game_over()

    def get_damage(self):
        distance = self.calculate_distance_between_tanks()
        if distance <= 250:
            return 30
        elif distance <= 500:
            return 20
        elif distance <= 750:
            return 15
        else:
            return 10  # Базове значення, якщо більше 750 пікселів

    def calculate_distance_between_tanks(self):
        player_center = self.get_tank_center(self.square)
        enemy_center = self.get_tank_center(self.enemy_square)
        return math.sqrt((player_center[0] - enemy_center[0]) ** 2 + (player_center[1] - enemy_center[1]) ** 2)

    def update_damage_based_on_distance(self):
        self.screen.after(100, self.update_damage_based_on_distance)  # Викликаємо функцію кожні 100 мс

    def spawn_boost(self):
        x = random.randint(edge_distance_width + 50, board_width - 50)
        y = random.randint(edge_distance_height + 50, board_height - 50)
        boost_type = random.choice(['speed', 'bullet', 'multi_shot'])
        if boost_type == 'speed':
            boost = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill='blue')
        elif boost_type == 'bullet':
            boost = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill='green')
        else:
            boost = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill='purple')
        self.boosts.append((boost, boost_type))
        self.screen.after(10000, self.spawn_boost)  # Спавн нового буста кожні 10 секунд
        self.screen.after(10000, lambda: self.remove_boost(boost))  # Видалення буста через 10 секунд

    def remove_boost(self, boost):
        for b, _ in self.boosts:
            if b == boost:
                self.canvas.delete(boost)
                self.boosts.remove((b, _))
                break

    def check_boost_collision(self):
        for boost, boost_type in self.boosts[:]:
            if self.check_collision_boost(boost, self.square):
                self.canvas.delete(boost)
                self.boosts.remove((boost, boost_type))
                self.apply_boost(self.square, boost_type)
            elif self.check_collision_boost(boost, self.enemy_square):
                self.canvas.delete(boost)
                self.boosts.remove((boost, boost_type))
                self.apply_boost(self.enemy_square, boost_type)

        self.screen.after(100, self.check_boost_collision)

    def check_collision_boost(self, boost, tank):
        boost_coords = self.canvas.coords(boost)
        tank_coords = self.canvas.coords(tank)
        boost_x1, boost_y1, boost_x2, boost_y2 = min(boost_coords[::2]), min(boost_coords[1::2]), max(boost_coords[::2]), max(boost_coords[1::2])
        tank_x1, tank_y1, tank_x2, tank_y2 = min(tank_coords[::2]), min(tank_coords[1::2]), max(tank_coords[::2]), max(tank_coords[1::2])
        return boost_x1 < tank_x2 and boost_x2 > tank_x1 and boost_y1 < tank_y2 and boost_y2 > tank_y1

    def apply_boost(self, tank, boost_type):
        if boost_type == 'speed':
            if tank == self.square:
                self.player_step_size = self.original_step_size * 2
                self.player_speed_boost_time = time.time()
            elif tank == self.enemy_square:
                self.enemy_step_size = self.original_step_size * 2
                self.enemy_speed_boost_time = time.time()
        elif boost_type == 'bullet':
            if tank == self.square:
                self.bullet_speed = self.original_bullet_speed * 1.5
                self.player_bullet_speed_boost_time = time.time()
            elif tank == self.enemy_square:
                self.bullet_speed = self.original_bullet_speed * 1.5
                self.enemy_bullet_speed_boost_time = time.time()
        elif boost_type == 'multi_shot':
            self.shoot_in_all_directions(tank)
        self.remove_boost_after_delay(boost_type)

    def remove_boost_after_delay(self, boost_type):
        current_time = time.time()
        if boost_type == 'speed':
            if current_time - self.player_speed_boost_time >= 5:
                self.player_step_size = self.original_step_size
            if current_time - self.enemy_speed_boost_time >= 5:
                self.enemy_step_size = self.original_step_size
        elif boost_type == 'bullet':
            if current_time - self.player_bullet_speed_boost_time >= 5:
                self.bullet_speed = self.original_bullet_speed
            if current_time - self.enemy_bullet_speed_boost_time >= 5:
                self.bullet_speed = self.original_bullet_speed

        self.screen.after(100, lambda: self.remove_boost_after_delay(boost_type))

    def spawn_bushes(self):
        self.bushes = []
        for _ in range(8):
            x = random.randint(edge_distance_width + 50, board_width - 50)
            y = random.randint(edge_distance_height + 50, board_height - 50)
            bush = self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill='darkgreen')
            self.bushes.append(bush)

    def hide_tank_in_bush(self, tank):
        for bush in self.bushes:
            if self.check_collision_boost(tank, bush):
                self.canvas.itemconfig(tank, state='hidden')
                return
        self.canvas.itemconfig(tank, state='normal')

    def show_tank(self, tank):
        self.canvas.itemconfig(tank, state='normal')

    def game_over(self):
        winner = "Player" if self.enemy_hp <= 0 else "Enemy"
        self.canvas.create_text(board_width // 2, board_height // 2, text=f"{winner} Wins!", font=("Arial", 50), fill="red")

        # Додавання кнопки для перезапуску гри
        self.restart_button = Button(self.screen, text="Рестарт", command=self.restart_game, bg=botton_color,
                                     width=12, height=4)
        self.restart_button.place(x=20, y=120)

    def restart_game(self):
        self.canvas.delete("all")  # Очистка канвасу
        self.keys_pressed = {key: False for key in self.keys_pressed}
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.boosts.clear()
        self.bushes.clear()
        self.last_shot_time_player = 0
        self.last_shot_time_enemy = 0
        self.player_speed_boost_time = 0
        self.enemy_speed_boost_time = 0
        self.player_bullet_speed_boost_time = 0
        self.enemy_bullet_speed_boost_time = 0

        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.player_step_size = self.original_step_size
        self.enemy_step_size = self.original_step_size
        self.bullet_speed = self.original_bullet_speed
        self.player_angle = player_angle  # Встановлюємо початковий кут повороту танка гравця
        self.enemy_angle = enemy_angle  # Встановлюємо початковий кут повороту ворожого танка

        # Відтворення ігрових елементів
        self.playing_board = self.canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                                          outline=outline_color, width=outline_width, fill=board_color)

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

        self.create_square()
        self.create_enemy_square()

        # Приховання кнопки рестарту
        self.restart_button.place_forget()

        # Перезапускаємо спавн бустів
        self.spawn_boost()
        self.check_boost_collision()

        # Перезапускаємо спавн кущів
        self.spawn_bushes()

    def exit_game(self):
        self.screen.destroy()

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    screen.mainloop()
