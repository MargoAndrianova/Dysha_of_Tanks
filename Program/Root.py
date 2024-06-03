from tkinter import *
from PIL import Image, ImageTk
import time
import math
import random
from Params import *

class Dysha_of_Tanks:
    def __init__(self, screen, player_name, enemy_name):
        self.screen = screen
        self.screen.attributes('-fullscreen', True)

        self.canvas = Canvas(self.screen, width=screen.winfo_screenwidth(), height=screen.winfo_screenheight())
        self.canvas.pack(fill=BOTH, expand=True)

        # Завантаження зображення фону
        self.background_image = Image.open('grace.png')
        self.background_image = self.background_image.resize((950, 575), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Встановлення фону
        self.canvas.create_image(edge_distance_width, edge_distance_height, image=self.background_photo, anchor=NW)

        self.player_name = player_name
        self.enemy_name = enemy_name

        self.playing_board = self.canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                                          outline=outline_color, width=outline_width, fill='')

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
        self.craters = []

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

        # Завантаження зображення танка
        self.original_tank_image = Image.open('tank.png')
        self.original_tank_image = self.original_tank_image.resize((self.square_size, self.square_size), Image.LANCZOS)
        self.player_tank_photo = ImageTk.PhotoImage(self.original_tank_image)
        self.enemy_tank_photo = ImageTk.PhotoImage(self.original_tank_image)

        # Завантаження зображення бустів
        self.speed_boost_image = Image.open('speed_boost.png')
        self.speed_boost_image = self.speed_boost_image.resize((40, 40), Image.LANCZOS)
        self.speed_boost_photo = ImageTk.PhotoImage(self.speed_boost_image)

        self.bullet_speed_boost_image = Image.open('bullet_speed_boost.png')
        self.bullet_speed_boost_image = self.bullet_speed_boost_image.resize((40, 40), Image.LANCZOS)
        self.bullet_speed_boost_photo = ImageTk.PhotoImage(self.bullet_speed_boost_image)

        self.multi_shot_boost_image = Image.open('multi_shot_boost.png')
        self.multi_shot_boost_image = self.multi_shot_boost_image.resize((40, 40), Image.LANCZOS)
        self.multi_shot_boost_photo = ImageTk.PhotoImage(self.multi_shot_boost_image)

        # Завантаження зображення кулі
        self.original_bullet_image = Image.open('tank_bullet.png')
        self.bullet_image = self.original_bullet_image.resize((30, 10), Image.LANCZOS)

        # Завантаження зображення кратера
        self.crater_image = Image.open('crator.png')
        self.crater_image = self.crater_image.resize((40, 40), Image.LANCZOS)
        self.crater_photo = ImageTk.PhotoImage(self.crater_image)

        # Завантаження зображення переможця
        self.winner_image = Image.open('winner.png')
        self.winner_image = self.winner_image.resize((400, 400), Image.LANCZOS)
        self.winner_photo = ImageTk.PhotoImage(self.winner_image)

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

        self.player_hp_text = self.canvas.create_text(edge_distance_width + self.hp_length + 100, edge_distance_height - self.hp_height / 2 - 10,
                                                      text=f'{self.player_name} HP: {self.player_hp}', font=('Arial', 14), fill='black')
        self.enemy_hp_text = self.canvas.create_text(board_width - self.hp_length - 100, board_height + 20 + self.hp_height / 2,
                                                     text=f'{self.enemy_name} HP: {self.enemy_hp}', font=('Arial', 14), fill='black')

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

        self.create_tank()
        self.create_enemy_tank()

        self.move_bullets()
        self.move_enemy_bullets()
        self.check_bullet_collision()
        self.update_movement()
        self.check_tank_collision()
        self.update_damage_based_on_distance()
        self.spawn_boost()
        self.check_boost_collision()
        self.check_crater_collision()

    def create_tank(self):
        x, y = tank_coords
        self.player_tank = self.canvas.create_image(x, y, image=self.player_tank_photo)

    def create_enemy_tank(self):
        x, y = enemy_coords
        self.enemy_tank = self.canvas.create_image(x, y, image=self.enemy_tank_photo)

    def rotate_image(self, image, angle):
        return ImageTk.PhotoImage(image.rotate(angle, expand=True))

    def handle_key_press(self, event):
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed[key] = True
        if key.lower() == 'shift_l':
            self.shoot(self.player_tank, self.player_angle)  # Стріляє в напрямку руху
        if key.lower() == 'shift_r':
            self.shoot_enemy(self.enemy_tank, self.enemy_angle)  # Стріляє в напрямку руху

    def handle_key_release(self, event):
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed[key] = False

    def disable_key(self, event):
        return "break"

    def update_movement(self):
        self.update_player_direction()
        self.update_enemy_direction()

        self.move_tank(self.player_tank, self.player_angle, self.player_direction, self.player_step_size)
        self.move_tank(self.enemy_tank, self.enemy_angle, self.enemy_direction, self.enemy_step_size)

        self.screen.after(50, self.update_movement)

    def update_player_direction(self):
        self.player_direction = {'x': 0, 'y': 0}
        if self.keys_pressed['s']:
            self.player_direction['y'] = -self.player_step_size
        if self.keys_pressed['w']:
            self.player_direction['y'] = self.player_step_size
        if self.keys_pressed['a']:
            self.player_angle -= angle_turn  # Поворот вліво
            self.update_tank_rotation(self.player_tank, self.player_angle, True)
        if self.keys_pressed['d']:
            self.player_angle += angle_turn  # Поворот вправо
            self.update_tank_rotation(self.player_tank, self.player_angle, True)

    def update_enemy_direction(self):
        self.enemy_direction = {'x': 0, 'y': 0}
        if self.keys_pressed['Down']:
            self.enemy_direction['y'] = -self.enemy_step_size
        if self.keys_pressed['Up']:
            self.enemy_direction['y'] = self.enemy_step_size
        if self.keys_pressed['Left']:
            self.enemy_angle -= angle_turn  # Поворот вліво
            self.update_tank_rotation(self.enemy_tank, self.enemy_angle, False)
        if self.keys_pressed['Right']:
            self.enemy_angle += angle_turn  # Поворот вправо
            self.update_tank_rotation(self.enemy_tank, self.enemy_angle, False)

    def move_tank(self, tank, angle, direction, step_size):
        rad = math.radians(angle)
        dx = direction['y'] * math.cos(rad) - direction['x'] * math.sin(rad)
        dy = direction['y'] * math.sin(rad) + direction['x'] * math.cos(rad)

        self.canvas.move(tank, dx, dy)
        self.limit_movement(tank)
        self.prevent_tank_overlap()

    def update_tank_rotation(self, tank, angle, is_player):
        if is_player:
            rotated_image = self.rotate_image(self.original_tank_image, -angle)
            self.player_tank_photo = rotated_image
            self.canvas.itemconfig(tank, image=rotated_image)
        else:
            rotated_image = self.rotate_image(self.original_tank_image, -angle)
            self.enemy_tank_photo = rotated_image
            self.canvas.itemconfig(tank, image=rotated_image)
        self.canvas.coords(tank, self.canvas.coords(tank)[0], self.canvas.coords(tank)[1])

    def get_tank_center(self, tank):
        coords = self.canvas.coords(tank)
        if not coords:
            return None, None
        x = coords[0]
        y = coords[1]
        return x, y

    def limit_movement(self, tank):
        coords = self.canvas.bbox(tank)
        if not coords:
            return
        x1, y1, x2, y2 = coords
        if x1 < edge_distance_width:
            self.canvas.move(tank, edge_distance_width - x1, 0)
        if y1 < edge_distance_height:
            self.canvas.move(tank, 0, edge_distance_height - y1)
        if x2 > board_width:
            self.canvas.move(tank, board_width - x2, 0)
        if y2 > board_height:
            self.canvas.move(tank, 0, board_height - y2)

    def limit_bullet(self, object):
        coords = self.canvas.bbox(object)
        if not coords:
            return
        x1, y1, x2, y2 = coords
        if x1 <= edge_distance_width - outline_width or x2 >= board_width - outline_width or y1 <= edge_distance_height - outline_width or y2 >= board_height - outline_width:
            self.canvas.delete(object)
            if object in [bullet[0] for bullet in self.bullets]:
                self.bullets = [bullet for bullet in self.bullets if bullet[0] != object]
            else:
                self.enemy_bullets = [bullet for bullet in self.enemy_bullets if bullet[0] != object]

    def shoot(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_player >= 1:
            bullet_image = self.rotate_image(self.bullet_image, -angle)
            bullet = self.canvas.create_image(*self.get_tank_front(tank, angle), image=bullet_image)
            self.bullets.append((bullet, angle, bullet_image))
            self.last_shot_time_player = current_time

    def shoot_enemy(self, tank, angle):
        current_time = time.time()
        if current_time - self.last_shot_time_enemy >= 1:
            bullet_image = self.rotate_image(self.bullet_image, -angle)
            bullet = self.canvas.create_image(*self.get_tank_front(tank, angle), image=bullet_image)
            self.enemy_bullets.append((bullet, angle, bullet_image))
            self.last_shot_time_enemy = current_time

    def shoot_in_all_directions(self, tank):
        directions = [0, 45, 90, 135, 180, 225, 270, 315]
        for angle in directions:
            bullet_image = self.rotate_image(self.bullet_image, -angle)
            bullet = self.canvas.create_image(*self.get_tank_front(tank, angle), image=bullet_image)
            self.bullets.append((bullet, angle, bullet_image))

    def get_tank_front(self, tank, angle):
        x, y = self.get_tank_center(tank)
        if x is None or y is None:
            return 0, 0
        rad = math.radians(angle)
        front_x = x + (tank_size / 2) * math.cos(rad)
        front_y = y + (tank_size / 2) * math.sin(rad)
        return front_x, front_y

    def move_bullets(self):
        for bullet, angle, _ in self.bullets[:]:
            self.move_bullet(bullet, angle)
        self.screen.after(bullet_interval, self.move_bullets)

    def move_enemy_bullets(self):
        for bullet, angle, _ in self.enemy_bullets[:]:
            self.move_bullet(bullet, angle)
        self.screen.after(bullet_interval, self.move_enemy_bullets)

    def move_bullet(self, bullet, angle):
        rad = math.radians(angle)
        dx = self.bullet_speed * math.cos(rad)
        dy = self.bullet_speed * math.sin(rad)
        self.canvas.move(bullet, dx, dy)
        self.limit_bullet(bullet)

    def check_bullet_collision(self):
        for bullet, _, _ in self.bullets[:]:
            if self.check_collision(bullet, self.enemy_tank):
                self.canvas.delete(bullet)
                self.bullets = [b for b in self.bullets if b[0] != bullet]
                self.enemy_hp -= self.get_damage()
                self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)
                self.create_crater(self.get_tank_center(self.enemy_tank))

        for bullet, _, _ in self.enemy_bullets[:]:
            if self.check_collision(bullet, self.player_tank):
                self.canvas.delete(bullet)
                self.enemy_bullets = [b for b in self.enemy_bullets if b[0] != bullet]
                self.player_hp -= self.get_damage()
                self.update_hp_bar(self.player_hp_fill, self.player_hp, self.player_hp_text)
                self.create_crater(self.get_tank_center(self.player_tank))

        self.screen.after(bullet_interval, self.check_bullet_collision)

    def check_collision(self, bullet, tank):
        bullet_coords = self.canvas.bbox(bullet)
        tank_coords = self.canvas.bbox(tank)
        if not bullet_coords or not tank_coords:
            return False
        bullet_x1, bullet_y1, bullet_x2, bullet_y2 = bullet_coords
        tank_x1, tank_y1, tank_x2, tank_y2 = tank_coords
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
        player_coords = self.canvas.bbox(self.player_tank)
        enemy_coords = self.canvas.bbox(self.enemy_tank)
        if not player_coords or not enemy_coords:
            return False
        player_x1, player_y1, player_x2, player_y2 = player_coords
        enemy_x1, enemy_y1, enemy_x2, enemy_y2 = enemy_coords
        return player_x1 < enemy_x2 and player_x2 > enemy_x1 and player_y1 < enemy_y2 and player_y2 > enemy_y1

    def reset_tanks(self):
        self.player_hp = max(self.player_hp - self.touch_damage, 0)
        self.enemy_hp = max(self.enemy_hp - self.touch_damage, 0)
        self.update_hp_bar(self.player_hp_fill, self.player_hp, self.player_hp_text)
        self.update_hp_bar(self.enemy_hp_fill, self.enemy_hp, self.enemy_hp_text)
        self.canvas.coords(self.player_tank, tank_coords[0], tank_coords[1])
        self.canvas.coords(self.enemy_tank, enemy_coords[0], enemy_coords[1])

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
        player_center = self.get_tank_center(self.player_tank)
        enemy_center = self.get_tank_center(self.enemy_tank)
        if None in (player_center, enemy_center):
            return float('inf')
        return math.sqrt((player_center[0] - enemy_center[0]) ** 2 + (player_center[1] - enemy_center[1]) ** 2)

    def update_damage_based_on_distance(self):
        self.screen.after(100, self.update_damage_based_on_distance)  # Викликаємо функцію кожні 100 мс

    def create_crater(self, coords):
        x, y = coords
        crater = self.canvas.create_image(x, y, image=self.crater_photo)
        self.craters.append(crater)
        self.screen.after(5000, lambda: self.remove_crater(crater))

    def remove_crater(self, crater):
        self.canvas.delete(crater)
        self.craters.remove(crater)

    def check_crater_collision(self):
        for crater in self.craters:
            if self.check_collision_with_crater(self.player_tank, crater):
                self.player_step_size = self.original_step_size // 2  # Зменшуємо швидкість гравця
                self.screen.after(1500, self.reset_player_speed)  # Відновлюємо швидкість через 1.5 секунду
            if self.check_collision_with_crater(self.enemy_tank, crater):
                self.enemy_step_size = self.original_step_size // 2  # Зменшуємо швидкість ворога
                self.screen.after(1500, self.reset_enemy_speed)  # Відновлюємо швидкість через 1.5 секунду
        self.screen.after(100, self.check_crater_collision)

    def check_collision_with_crater(self, tank, crater):
        tank_coords = self.canvas.bbox(tank)
        crater_coords = self.canvas.bbox(crater)
        if not tank_coords or not crater_coords:
            return False
        tank_x1, tank_y1, tank_x2, tank_y2 = tank_coords
        crater_x1, crater_y1, crater_x2, crater_y2 = crater_coords
        return tank_x1 < crater_x2 and tank_x2 > crater_x1 and tank_y1 < crater_y2 and tank_y2 > crater_y1

    def reset_player_speed(self):
        self.player_step_size = self.original_step_size

    def reset_enemy_speed(self):
        self.enemy_step_size = self.original_step_size

    def spawn_boost(self):
        x = random.randint(edge_distance_width + 50, board_width - 50)
        y = random.randint(edge_distance_height + 50, board_height - 50)
        boost_type = random.choice(['speed', 'bullet', 'multi_shot'])
        if boost_type == 'speed':
            boost = self.canvas.create_image(x, y, image=self.speed_boost_photo)
        elif boost_type == 'bullet':
            boost = self.canvas.create_image(x, y, image=self.bullet_speed_boost_photo)
        else:
            boost = self.canvas.create_image(x,y, image=self.multi_shot_boost_photo)
        self.boosts.append((boost, boost_type))
        self.screen.after(7000, self.spawn_boost)  # Спавн нового буста кожні 7 секунд
        self.screen.after(5000, lambda: self.remove_boost(boost))  # Видалення буста через 5 секунд

    def remove_boost(self, boost):
        for b, _ in self.boosts:
            if b == boost:
                self.canvas.delete(boost)
                self.boosts.remove((b, _))
                break

    def check_boost_collision(self):
        for boost, boost_type in self.boosts[:]:
            if self.check_collision_boost(boost, self.player_tank):
                self.canvas.delete(boost)
                self.boosts.remove((boost, boost_type))
                self.apply_boost(self.player_tank, boost_type)
            elif self.check_collision_boost(boost, self.enemy_tank):
                self.canvas.delete(boost)
                self.boosts.remove((boost, boost_type))
                self.apply_boost(self.enemy_tank, boost_type)

        self.screen.after(100, self.check_boost_collision)

    def check_collision_boost(self, boost, tank):
        boost_coords = self.canvas.bbox(boost)
        tank_coords = self.canvas.bbox(tank)
        if not boost_coords or not tank_coords:
            return False
        boost_x1, boost_y1, boost_x2, boost_y2 = boost_coords
        tank_x1, tank_y1, tank_x2, tank_y2 = tank_coords
        return boost_x1 < tank_x2 and boost_x2 > tank_x1 and boost_y1 < tank_y2 and boost_y2 > tank_y1

    def apply_boost(self, tank, boost_type):
        if boost_type == 'speed':
            if tank == self.player_tank:
                self.player_step_size = self.original_step_size * 1.5
                self.player_speed_boost_time = time.time()
            elif tank == self.enemy_tank:
                self.enemy_step_size = self.original_step_size * 1.5
                self.enemy_speed_boost_time = time.time()
        elif boost_type == 'bullet':
            if tank == self.player_tank:
                self.bullet_speed = self.original_bullet_speed * 2
                self.player_bullet_speed_boost_time = time.time()
            elif tank == self.enemy_tank:
                self.bullet_speed = self.original_bullet_speed * 2
                self.enemy_bullet_speed_boost_time = time.time()
        elif boost_type == 'multi_shot':
            if tank == self.player_tank:
                self.shoot_in_all_directions(self.player_tank)
            elif tank == self.enemy_tank:
                self.shoot_in_all_directions(self.enemy_tank)
        self.remove_boost_after_delay(boost_type)

    def remove_boost_after_delay(self, boost_type):
        current_time = time.time()
        if boost_type == 'speed':
            if current_time - self.player_speed_boost_time >= 3:
                self.player_step_size = self.original_step_size
            if current_time - self.enemy_speed_boost_time >= 3:
                self.enemy_step_size = self.original_step_size
        elif boost_type == 'bullet':
            if current_time - self.player_bullet_speed_boost_time >= 3:
                self.bullet_speed = self.original_bullet_speed
            if current_time - self.enemy_bullet_speed_boost_time >= 3:
                self.bullet_speed = self.original_bullet_speed

        self.screen.after(100, lambda: self.remove_boost_after_delay(boost_type))

    def game_over(self):
        winner = f"{self.player_name}" if self.enemy_hp <= 0 else f"{self.enemy_name}"
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()

        # Відображення зображення переможця
        self.canvas.create_image(screen_width // 2, screen_height // 2, image=self.winner_photo)

        # Відображення тексту переможця
        self.canvas.create_text(screen_width // 2, screen_height // 2 + 100, text=f"{winner} Wins!", font=("Arial", 50),
                                fill="red")


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
        self.craters.clear()
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

        self.background_image = Image.open('grace.png')
        self.background_image = self.background_image.resize((950, 575), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Встановлення фону
        self.canvas.create_image(edge_distance_width, edge_distance_height, image=self.background_photo, anchor=NW)

        # Відтворення ігрових елементів
        self.playing_board = self.canvas.create_rectangle(edge_distance_width, edge_distance_height, board_width, board_height,
                                                          outline=outline_color, width=outline_width, fill='')

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
                                                      text=f'{self.player_name} HP: {self.player_hp}', font=('Arial', 14), fill='black')
        self.enemy_hp_text = self.canvas.create_text(board_width - self.hp_length - 50, board_height + 20 + self.hp_height / 2,
                                                     text=f'{self.enemy_name} HP: {self.enemy_hp}', font=('Arial', 14), fill='black')

        self.create_tank()
        self.create_enemy_tank()

        # Приховання кнопки рестарту
        self.restart_button.place_forget()

        # Перезапускаємо спавн бустів
        self.spawn_boost()
        self.check_boost_collision()
        self.check_crater_collision()

    def exit_game(self):
        self.screen.destroy()