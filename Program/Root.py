from tkinter import *
from Params import *
import time

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

        self.screen.bind('<Escape>', lambda event: self.screen.quit())
        self.screen.bind('<KeyPress>', self.handle_key_press)
        self.screen.bind('<KeyRelease>', self.handle_key_release)

    def create_square(self):
        self.square = self.canvas.create_rectangle(tank_coords[0], tank_coords[1],
                                                   tank_coords[0] + tank_size, tank_coords[1] + tank_size,
                                                   fill=square_color)

    def create_enemy_square(self):
        self.enemy_square = self.canvas.create_rectangle(enemy_coords[0], enemy_coords[1],
                                                         enemy_coords[0] + tank_size, enemy_coords[1] + tank_size,
                                                         fill=enemy_color)

    def handle_key_press(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right'] or key.lower() in ['w', 's', 'a', 'd']:
            self.keys_pressed.add(key)
            self.screen.after(1, self.move_square)
        if key.lower() == 'shift_l':
            self.shoot()
        if key.lower() == 'shift_r':
            self.shoot_enemy()

    def handle_key_release(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right'] or key.lower() in ['w', 's', 'a', 'd']:
            self.keys_pressed.remove(key)

    def move_square(self):
        for key in self.keys_pressed:
            if key.lower() == 'w':
                self.canvas.move(self.square, 0, -self.step_size)
            if key.lower() == 's':
                self.canvas.move(self.square, 0, self.step_size)
            if key.lower() == 'a':
                self.canvas.move(self.square, -self.step_size, 0)
            if key.lower() == 'd':
                self.canvas.move(self.square, self.step_size, 0)
            if 'Up' == key:
                self.canvas.move(self.enemy_square, 0, -self.step_size)
            if 'Down' == key:
                self.canvas.move(self.enemy_square, 0, self.step_size)
            if 'Left' == key:
                self.canvas.move(self.enemy_square, -self.step_size, 0)
            if 'Right' == key:
                self.canvas.move(self.enemy_square, self.step_size, 0)

        self.limit_movement(self.square)
        self.limit_movement(self.enemy_square)

    def limit_movement(self, object):
        # Обмеження для танка
        x1, y1, x2, y2 = self.canvas.coords(object)
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
        if x1 <= edge_distance_width - outline_width:
            self.canvas.delete(object)
            self.bullets.remove(object)
        if y1 <= edge_distance_height - outline_width:
            self.canvas.delete(object)
            self.bullets.remove(object)
        if x2 >= board_width - outline_width:
            self.canvas.delete(object)
            self.bullets.remove(object)
        if y2 >= board_height - outline_width:
            self.canvas.delete(object)
            self.bullets.remove(object)

    def limit_enemy_bullet(self, object):
        x1, y1, x2, y2 = self.canvas.coords(object)
        if x1 <= edge_distance_width - outline_width:
            self.canvas.delete(object)
            self.enemy_bullets.remove(object)
        if y1 <= edge_distance_height - outline_width:
            self.canvas.delete(object)
            self.enemy_bullets.remove(object)
        if x2 >= board_width - outline_width:
            self.canvas.delete(object)
            self.enemy_bullets.remove(object)
        if y2 >= board_height - outline_width:
            self.canvas.delete(object)
            self.enemy_bullets.remove(object)

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time_player >= 1:
            x1, y1, x2, y2 = self.canvas.coords(self.square)
            self.bullet = self.canvas.create_rectangle((x1 + x2) // 2 - 2, y1 - bullet_speed, (x1 + x2) // 2 + 2, y1,
                                                       fill=bullet_color)
            self.bullets.append(self.bullet)
            self.last_shot_time_player = current_time

    def shoot_enemy(self):
        current_time = time.time()
        if current_time - self.last_shot_time_enemy >= 1:
            x1, y1, x2, y2 = self.canvas.coords(self.enemy_square)
            self.enemy_bullet = self.canvas.create_rectangle((x1 + x2) // 2 - 2, y1 - bullet_speed, (x1 + x2) // 2 + 2,
                                                             y1, fill=enemy_bullet_color)
            self.enemy_bullets.append(self.enemy_bullet)
            self.last_shot_time_enemy = current_time

    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -bullet_speed)
            self.limit_bullet(bullet)
        self.screen.after(bullet_interval, self.move_bullets)

    def move_enemy_bullets(self):
        for bullet in self.enemy_bullets[:]:
            self.canvas.move(bullet, 0, -bullet_speed)
            self.limit_enemy_bullet(bullet)
        self.screen.after(bullet_interval, self.move_enemy_bullets)

    def check_bullet_collision(self):
        # Перевірка попадання куль гравця у ворожий танк
        x1, y1, x2, y2 = self.canvas.coords(self.enemy_square)
        for bullet in self.bullets[:]:
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            if bx1 < x2 and bx2 > x1 and by1 < y2 and by2 > y1:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

        # Перевірка попадання куль ворога у танк гравця
        x1, y1, x2, y2 = self.canvas.coords(self.square)
        for bullet in self.enemy_bullets[:]:
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            if bx1 < x2 and bx2 > x1 and by1 < y2 and by2 > y1:
                self.canvas.delete(bullet)
                self.enemy_bullets.remove(bullet)

        self.screen.after(bullet_interval, self.check_bullet_collision)

    def exit_game(self):
        self.screen.destroy()

if __name__ == '__main__':
    screen = Tk()
    dysha = Dysha_of_Tanks(screen)
    dysha.create_square()
    dysha.create_enemy_square()
    dysha.move_bullets()
    dysha.move_enemy_bullets()
    dysha.check_bullet_collision()
    screen.mainloop()