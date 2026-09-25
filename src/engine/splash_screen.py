import pygame
from .load_gifs import load_gif_frames


class DrawSplash:
    """
    Handles the rendering and animation sequence for the game splash screen.
    Displays animated sprites including Pac-Man, ghosts, and pac-gums.
    """
    def __init__(self, WIDTH, HEIGHT, screen, colors):
        """
        Initializes splash screen dimensions, target display screen, and color theme.
        """
        self.width = WIDTH
        self.height = HEIGHT
        self.view_splash = True
        self.screen = screen

        self.colors = colors

    def draw_pacgums(self, x, y, number):
        """
        Renders a horizontal row of pac-gum circles on the screen.
        Decreases the number of gums drawn as Pac-Man eats them.
        """
        x = 1240
        while number > 0:
            x -= 20
            pygame.draw.circle(self.screen,
                               self.colors['yellow'], (x, y + 25),
                               radius=3)
            number -= 1

    def draw_pacman(self, x, y, step, image):
        """
        Scales and renders Pac-Man's animation frame at its current position.
        Returns True if Pac-Man moves beyond the right screen boundary, else False.
        """
        x += step - 360
        if x >= 1430:
            return True
        self.screen.blit(pygame.transform.scale(image, (30, 30)), (x, y + 10))
        return False

    def draw_ghosts(self, x, y, step, image):
        """
        Scales and renders a ghost's animation frame following Pac-Man's movement path.
        """
        x += step - 360
        self.screen.blit(pygame.transform.scale(image, (30, 30)), (x, y + 10))

    def show_splash(self):
        """
        Runs the splash screen main animation loop, handling frame updates,
        sprite loading, and rendering sequence for Pac-Man, ghosts, and pac-gums.
        """
        center_x = self.width // 2
        center_y = self.height // 2
        pacman_frame = 0
        yellow_frame = 0
        blue_frame = 0
        red_frame = 0
        walk_speed = 20
        nb_pacgum = 26
        pacman_frames = load_gif_frames('./assists/images/pacman.gif')
        yellow_ghost = load_gif_frames('./assists/images/yellowghost.gif')
        blue_ghost = load_gif_frames('./assists/images/blueghost.gif')
        red_ghost = load_gif_frames('./assists/images/redghost.gif')
        while self.view_splash:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill(self.colors["background"])
            pac_image = pacman_frames[pacman_frame]
            pacman_frame = (pacman_frame + 1) % len(pacman_frames)
            yellow_frame = (yellow_frame + 1) % len(yellow_ghost)
            blue_frame = (blue_frame + 1) % len(blue_ghost)
            red_frame = (red_frame + 1) % len(red_ghost)
            pygame.draw.rect(self.screen,
                             self.colors["dark"],
                             (center_x - 489 // 2, center_y + 6, 489, 39),
                             border_radius=4)
            if walk_speed >= 100:
                self.draw_ghosts(center_x, center_y, walk_speed - 60,
                                 yellow_ghost[yellow_frame])
                self.draw_ghosts(center_x, center_y, walk_speed - 110,
                                 blue_ghost[blue_frame])
                self.draw_ghosts(center_x, center_y, walk_speed - 160,
                                 red_ghost[red_frame])
                nb_pacgum -= 1
            self.draw_pacgums(center_x, center_y, nb_pacgum)
            if self.draw_pacman(center_x, center_y, walk_speed, pac_image):
                break
            pygame.draw.rect(self.screen,
                             self.colors["yellow"],
                             (center_x - 500 // 2, center_y, 500, 50),
                             width=6,
                             border_radius=10)

            pygame.draw.rect(self.screen, self.colors["background"],
                             (center_x - 520, center_y - 17, 270, 70))
            pygame.draw.rect(self.screen, self.colors["background"],
                             (center_x + 250, center_y - 17, 270, 70))
            pygame.display.update()
            walk_speed += 20
            pygame.time.wait(100)
