import pygame
from pygame.locals import *
import sys

class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.jump = False
        self.jump_counter = 0

    def move_left(self, map_data, map_now, size):
        if int(self.map.check_collision(self.x - map_now + size / 2, self.y, -1, 0, size)) != 1:
            if map_now < 0 and self.y == 366:
                map_now += 1
            elif self.y > 5:
                self.y -= 1
            self.direction = 2

    def move_right(self, map_data, map_now, size):
        if int(self.map.check_collision(self.x - map_now + size / 2, self.y, -1, 0, size)) != 1:
            if map_now > -4100 and self.y == 366:
                map_now -= 1
            elif self.y < 990:
                self.y += 1
            self.direction = 1

    def jump_logic(self, map_data, map_now, size):
        if not self.jump:
            if map.check_collision(self.x - map_now, self.y - size / 2, 0, 1, size) != 1:
                if map.check_collision(self.x - map_now, self.y - size / 2, 0, 1, size) != 1:
                    self.x += 1
            if map.check_collision(self.x - map_now, self.y - size / 2, 0, 1, size) == 1:
                self.jump_counter = 0
                self.jump = True

        if self.jump:
            self.x -= 1
            self.jump_counter += 1
            if self.jump_counter > 150:
                self.jump = False
            if map.check_collision(self.x - map_now, self.y + size / 2, 0, -1, size) == 1:
                if map.check_collision(self.x - map_now, self.y + size / 2, 0, -1, size) == 1:
                    self.jump = False

    def draw(self, screen, color, box_size):
        pygame.draw.circle(screen, color, (self.y, self.x), box_size / 2)


class Map:
    def __init__(self, data):
        self.data = data

    def make(self, screen, map_now, size):
        block_y = 0
        block_x = 0
        while block_y < 20:
            while block_x < 200:
                if self.data[block_y][block_x] == 1:
                    pygame.draw.rect(screen, (0, 0, 255), Rect(map_now + (size * block_x), (size * block_y), size, size))
                elif self.data[block_y][block_x] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), Rect(map_now + (size * block_x), (size * block_y), size, size))
                block_x += 1
            block_y += 1
            block_x = 0

    def check_collision(self, x_now, y_now, next_x, next_y, size):
        x_arr = x_now / size
        y_arr = y_now / size
        return self.data[int(y_arr + next_y)][int(x_arr + next_x)]


class Game:
    def __init__(self):
        self.width = 1000
        self.height = 520
        self.map_now = 0
        self.player_x_now = 400
        self.player_y_now = 200
        self.player_direction = 1
        self.box_size = 26
        self.stage_setup = [0, 400, 200, 1, False]
        self.map_data = []

        pygame.init()
        pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("main")
        self.screen = pygame.display.get_surface()

        tmp = open('map.txt', 'r')
        while True:
            data_y = tmp.readline()
            if data_y == '':
                break
            data_in = data_y.split()
            data_x = [int(i) for i in data_in]
            self.map_data.append(data_x)

        self.player = Player(self.player_x_now, self.player_y_now, self.player_direction)
        self.map = Map(self.map_data)

    def main_loop(self):
        while True:
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.height))
            self.map.make(self.screen, self.map_now, self.box_size)
            pressed_key = pygame.key.get_pressed()

            if pressed_key[K_a]:
                self.player.move_left(self.map_data, self.map_now, self.box_size)
            if pressed_key[K_d]:
                self.player.move_right(self.map_data, self.map_now, self.box_size)
            if pressed_key[K_SPACE]:
                self.player.jump_logic(self.map_data, self.map_now, self.box_size)

            self.player.draw(self.screen, (0, 255, 0), self.box_size)

            pygame.display.update()
            pygame.time.wait(1)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main_loop()
