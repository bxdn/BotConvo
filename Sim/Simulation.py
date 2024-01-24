import os
from datetime import datetime
from math import atan2, cos, sin
from random import randint

import arcade as arcade
from arcade import load_texture

screen_width = 500
screen_height = 500

close_threshold = 5
ppf = 7

scale = 4
tile_size = 16 * scale
min_x = 50
min_y = 50
max_x = 480
max_y = 480

min_char_x = min_x + tile_size
min_char_y = min_y + 1.5 * tile_size
max_char_x = max_x - 1.5 * tile_size
max_char_y = max_y - tile_size

num_others = 5

files = ['char', 'clothes', 'pants', 'hair']
directions = ['down', 'up', 'right', 'left']


def _choose_interior_file(x, y):
    if y == min_y:
        if x == min_x:
            return 'border_6.png'
        elif x + tile_size >= max_x:
            return 'border_8.png'
        else:
            return 'border_7.png'
    elif y + tile_size >= max_y:
        if x == min_x:
            return 'border_1.png'
        elif x + tile_size >= max_x:
            return 'border_3.png'
        else:
            return 'border_2.png'
    elif x == min_x:
        return 'border_4.png'
    elif x + tile_size >= max_x:
        return 'border_5.png'
    else:
        return 'floor_1.png'


class Character:
    """
    Class for character sprites
    """

    def __init__(self, x, y):
        self.sprites = []
        for file in files:
            textures = []
            for direction in directions:
                for i in range(1, 9):
                    textures.append(
                        load_texture(os.path.join('Sim', 'assets', 'character', direction, f'{file}_{i}.png')))
            new_sprite = arcade.Sprite(texture=textures[0], scale=scale, center_x=x, center_y=y)
            self.sprites.append(new_sprite)
            new_sprite.textures = textures

        self.sprite_count = 0
        self.last_time_move = datetime.now()
        self.last_time_animate = datetime.now()
        self.destination = (x, y)
        self.direction = 'down'

    def update(self):
        time = datetime.now()
        if (time - self.last_time_move).total_seconds() > 0.02 and not self.is_close():
            self.last_time_move = time
            for sprite in self.sprites:
                self._update_movement(sprite)
        if (time - self.last_time_animate).total_seconds() > 0.075:
            self.last_time_animate = time
            self._update_animation()

    def draw(self):
        for sprite in self.sprites:
            sprite.draw()

    def _update_movement(self, sprite):
        pos = (sprite.center_x, sprite.center_y)
        vertical = abs(pos[0] - self.destination[0]) < abs(pos[1] - self.destination[1])
        if vertical:
            self.direction = 'up' if pos[1] < self.destination[1] else 'down'
        else:
            self.direction = 'right' if pos[0] < self.destination[0] else 'left'
        theta_radians = atan2(self.destination[1] - pos[1], self.destination[0] - pos[0])
        sprite.center_x = min(max(min_char_x, sprite.center_x + cos(theta_radians) * ppf), max_char_y)
        sprite.center_y = min(max(min_char_y, sprite.center_y + sin(theta_radians) * ppf), max_char_y)

    def _update_animation(self):
        if not self.is_close():
            self.sprite_count += 1
            if self.sprite_count == 8:
                self.sprite_count = 0
        else:
            self.sprite_count = 0
        for sprite in self.sprites:
            sprite.set_texture(directions.index(self.direction) * 8 + self.sprite_count)

    def is_close(self):
        for sprite in self.sprites:
            if abs(sprite.center_x - self.destination[0]) < close_threshold and abs(
                    sprite.center_y - self.destination[1]) < close_threshold:
                return True
        return False


class Background:
    def __init__(self):
        self.sprites = []
        for i in range(min_y, max_y, tile_size):
            for j in range(min_x, max_x, tile_size):
                file = _choose_interior_file(j, i)
                self.sprites.append(
                    arcade.Sprite(os.path.join('Sim', 'assets', 'interior', file), scale=scale, center_x=j, center_y=i))
        self.sprites.append(arcade.Sprite(os.path.join('Sim', 'assets', 'interior', 'laptop_desk.png'), scale=scale, center_x=min_x + tile_size * 2, center_y=max_y - 0.5 * tile_size))
        self.sprites.append(arcade.Sprite(os.path.join('Sim', 'assets', 'interior', 'couch_table.png'), scale=scale,
                                      center_x=max_x - tile_size * 3.25, center_y=min_y + tile_size * 1.5))

    def draw(self):
        for sprite in self.sprites:
            sprite.draw()


class Simulation(arcade.Window):
    """
    Window class for all GUI-side code
    """

    def __init__(self, service_provider):
        super().__init__(screen_width, screen_height, 'Simulation!')
        self._service_provider = service_provider
        self.background = Background()
        self.player = Character(100, 200)
        self.others = [(randint(1, 600), Character(randint(min_char_x, max_char_x), randint(min_char_y, max_char_y))) for _ in range(num_others)]
        self.pressed = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.player.destination = (x, y)
        self.pressed = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.pressed = False

    def on_mouse_motion(self, x, y, z, a):
        if self.pressed:
            self.player.destination = (x, y)

    def on_update(self, delta_time: float):
        for i, other_tuple in enumerate(self.others):
            countdown, other = other_tuple
            if countdown == 0:
                other.destination = (randint(min_char_x, max_char_x), randint(min_char_y, max_char_y))
                self.others[i] = (randint(1, 600), other)
            elif other.is_close():
                self.others[i] = (countdown - 1, other)
            other.update()
        self.player.update()

    def on_draw(self):
        self.clear()
        self.background.draw()
        characters = [self.player, *[other_tuple[1] for other_tuple in self.others]]
        characters.sort(key=lambda char: char.sprites[0].center_y, reverse=True)
        for character in characters:
            character.draw()
