import pygame
from pygame.locals import *
import sys

class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move_left(self, game):
        if game.map_now <= 0:
            game.map_now += 1

    def move_right(self, game):
        if game.map_now >= - (len(game.map_data[0]) * game.box_size) + game.width:
            game.map_now -= 1

    def jump(self):
        # Jump logic
        pass

    def fall(self):
        # Fall logic
        pass

    def draw(self, screen):
        # Draw player logic
        pass

class Map:
    def __init__(self, data):
        self.data = data

    def make(self, game):
        height = len(game.map_data)
        width = len(game.map_data[0])

        for block_y in range(height):
            for block_x in range(width):
                if game.map_data[block_y][block_x] == 1:
                    pygame.draw.rect(game.screen, (0, 0, 255), Rect((game.map_now + game.box_size * block_x), (game.box_size * block_y), game.box_size, game.box_size))
                elif game.map_data[block_y][block_x] == 2:
                    pygame.draw.rect(game.screen, (255, 0, 0), Rect((game.map_now + game.box_size * block_x), (game.box_size * block_y), game.box_size, game.box_size))

    def check_collision(self, x_now, y_now, next_x, next_y, size):
        # Collision detection logic
        pass

    def restart(self, setup):
        # Restart logic
        pass

class Game:
    def __init__(self):
        self.width = 1040
        self.height = 520
        self.player_x_now = 400
        self.player_y_now = 200
        self.player_direction = 1
        self.map_now = 0
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
            self.map.make(self)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pressed_key = pygame.key.get_pressed()

            if pressed_key[K_a]:
                self.player.move_left(self)
                
            if pressed_key[K_d]:
                self.player.move_right(self)
            
            if pressed_key[K_ESCAPE]:
                pygame.quit()
                sys.exit()            

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.main_loop()
