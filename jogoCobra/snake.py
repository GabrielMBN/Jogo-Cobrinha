import pygame
from pygame.locals import *
import time
import random
import glob


HEIGHT = 720
WIDTH = 960
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_list = glob.glob('resources/apple*.jpg')
        self.image = pygame.image.load(self.apple_list[random.randint(0, len(self.apple_list) - 1)]).convert()
        self.x = random.randint(1, int(WIDTH/SIZE) - 1)*SIZE
        self.y = random.randint(1, int(HEIGHT/SIZE) - 1)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.image = pygame.image.load(self.apple_list[random.randint(0, len(self.apple_list) - 1)]).convert()
        self.x = random.randint(1, int(WIDTH / SIZE) - 1) * SIZE
        self.y = random.randint(1, int(HEIGHT / SIZE) - 1) * SIZE

class cobra:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.head = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update corpo
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update cabeça
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            blockType = self.image
            if i == 0:
                blockType = self.head
            self.parent_screen.blit(blockType, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.image = pygame.image.load("resources/block2.jpg").convert()
        self.length += 1
        self.x.append(40)
        self.y.append(40)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Joguim de cobra :D")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.cobra = cobra(self.surface)
        self.cobra.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.cobra = cobra(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        # if x2 <= x1 < x2 + SIZE:
        #     if y2 <= y1 < y2 + SIZE:
        #         return True
        # return False
        return x1 == x2 and y1 == y2

    def wall_collision(self, y, x):
        if ((x >= WIDTH) or (y >= HEIGHT)) or ((x < 0) or (y < 0)):
            return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.apple.draw()
        self.cobra.walk()
        self.display_score()
        pygame.display.flip()

        # cobra come maca
        if self.is_collision(self.cobra.x[0], self.cobra.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.cobra.increase_length()
            self.apple.move()

        # cobra bate em si mesma
        for i in range(3, self.cobra.length):
            if self.is_collision(self.cobra.x[0], self.cobra.y[0], self.cobra.x[i], self.cobra.y[i]):
                self.play_sound('crash')
                pause = True
                raise 'Bateu!'
                self.show_game_over()

        if self.wall_collision:
            if self.wall_collision(self.cobra.y[0], self.cobra.x[0]):
                self.play_sound('crash')
                pause = True
                raise 'Bateu!'
                self.show_game_over()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.cobra.length}",True,(200,200,200))
        self.surface.blit(score, ((WIDTH - score.get_width() - 10), 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Sua pontuação é: {self.cobra.length}", True, (255, 255, 255))
        self.surface.blit(line1, (400, 350))
        line2 = font.render("Aperte ENTER para reiniciar ou ESC para sair!", True, (255, 255, 255))
        self.surface.blit(line2, (250, 400))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.cobra.move_left()

                        if event.key == K_RIGHT:
                            self.cobra.move_right()

                        if event.key == K_UP:
                            self.cobra.move_up()

                        if event.key == K_DOWN:
                            self.cobra.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.16)

if __name__ == '__main__':
    game = Game()
    game.run()