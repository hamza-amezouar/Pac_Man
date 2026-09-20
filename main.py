import time

import pygame
from src.engine.splash_screen import DrawSplash

class Engine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./assists/audios/background.mp3")
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.colors = {
            "yellow": (255, 255, 0),
            "dark": (0, 0, 0),
            "deep_blue": (25, 25, 166),
            "blue": (33, 33, 222),
            "warm_peach": (222, 161, 133),
            "red": (253, 1, 0),
            "green": (0, 255, 1),
            "yellow_dark": (223, 124, 0)
            }
        self.draw_splash = DrawSplash(self.width, self.height, self.screen, self.colors)

    def run_engine(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.draw_splash.show_splash()
            self.screen.fill(self.colors["dark"])
            pygame.display.update()
            time.sleep(20)
            break

engine = Engine(1920, 1080)

engine.run_engine()