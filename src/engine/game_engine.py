import pygame
import time
from PIL import Image, ImageSequence

class MenuManager:
    def __init__(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.view_splash = True
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./assists/audios/background.mp3")
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.colors = {
            "yellow": (255, 255, 0),
            "black": (0, 0, 0),
            "deep_blue": (25, 25, 166),
            "blue": (33, 33, 222),
            "warm_peach": (222, 161, 133),
            "red": (253, 1, 0),
            "green": (0, 255, 1)
            }
    def pacgums_splash(self, x, y, number):

        x = 1240
        while number > 0:
            x -= 20
            pygame.draw.circle(self.screen, self.colors['yellow'], (x, y + 25), radius=3)
            number -= 1

    def pacman_splash(self, x, y, step, image):
        x += step - 360
        if x >= 1430:
            return True
        self.screen.blit(pygame.transform.scale(image, (30, 30)), (x, y + 10))
        return False

    def ghost_spalsh(self, x, y, step, image):

        x += step - 360
        self.screen.blit(pygame.transform.scale(image, (30, 30)), (x, y + 10))

    def load_gif_frames(self, gif_path):
    
        git = Image.open(gif_path)
        frames = []
        for frame in ImageSequence.Iterator(git):
            frame_rgba = frame.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, "RGBA")
            frames.append(pygame_image)
        return frames

    def show_splash(self):

        center_x = self.width // 2
        center_y = self.height // 2
        pacman_frame = 0
        yellow_frame = 0
        blue_frame = 0
        red_frame = 0
        step = 20
        nb_pacgum = 26
        pacman_frames = self.load_gif_frames('./assists/images/pacman.gif')
        yellow_ghost = self.load_gif_frames('./assists/images/yellowghost.gif')
        blue_ghost = self.load_gif_frames('./assists/images/blueghost.gif')
        red_ghost = self.load_gif_frames('./assists/images/redghost.gif')
        while self.view_splash:
            keys = pygame.key.get_pressed()
            self.screen.fill(self.colors["yellow"])
            pac_image = pacman_frames[pacman_frame]
            pacman_frame = (pacman_frame + 1) % len(pacman_frames)
            yellow_frame = (yellow_frame + 1) % len(yellow_ghost)
            blue_frame = (blue_frame + 1) % len(blue_ghost)
            red_frame = (red_frame + 1) % len(red_ghost)
            pygame.draw.rect(
                self.screen, self.colors["black"],
                (center_x - 489 // 2, center_y + 6,
                 489, 39), border_radius=4)

            if step >= 100:
                self.ghost_spalsh(center_x, center_y, step - 60, yellow_ghost[yellow_frame])
                self.ghost_spalsh(center_x, center_y, step - 110, blue_ghost[blue_frame])
                self.ghost_spalsh(center_x, center_y, step - 160, red_ghost[red_frame])
                nb_pacgum -= 1
            self.pacgums_splash(center_x, center_y, nb_pacgum)
            if self.pacman_splash( center_x, center_y, step, pac_image):
                break
            pygame.draw.rect(
                self.screen, self.colors["blue"],
                (center_x - 500 // 2, center_y, 500, 50),
                width=6, border_radius=10)

            pygame.draw.rect(
                self.screen, self.colors["yellow"],
                (center_x - 520, center_y - 17, 270, 70))
            pygame.draw.rect(
                self.screen, self.colors["yellow"],
                (center_x + 250, center_y - 17, 270, 70))
            pygame.display.update()
            time.sleep(0.2)
            step += 20
            

    def show_main_menu(self):
        pass


engine =  MenuManager(1920, 1080)
engine.show_splash()
