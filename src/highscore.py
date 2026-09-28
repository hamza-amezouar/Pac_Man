import pygame


class Draw_highscores:

    def __init__(self, screen, colors, width, height, highscores):
        self.screen = screen
        self.width = width
        self.height = height
        self.highscors = highscores
        self.colors = colors
        self.buttons = []
        self.highscore_font = pygame.font.Font(
            "./assists/fonts/PixeloidSansBold-1jpBg.ttf", 40)
        self.name_font = pygame.font.Font(
            "./assists/fonts/Game Paused DEMO.otf", 20)
        self.rank_font = pygame.font.Font(None, 26)
        self.pts_font = pygame.font.Font("./assists/fonts/ka1.ttf", 20)
        self.bg_image = pygame.image.load('./assists/images/background.png')
        self.background = pygame.transform.scale(
            self.bg_image, (self.width, self.height)).convert()

    def draw_title(self):
        title_surface = self.highscore_font.render("HIGH SCORS TOP 10", True,
                                                   self.colors["yellow_dark"])
        title_rect = title_surface.get_rect()
        title_rect = (self.width // 2 - 200, 20)
        self.screen.blit(title_surface, title_rect)

    def draw_profiles_place(self):
        step = 0
        rank = 1
        current_image = 0
        profiles = [
            "/home/hamezoua/pac-man/assists/images/profiles/profile1.jpg",
            "/home/hamezoua/pac-man/assists/images/profiles/profile3.jpeg",
            "/home/hamezoua/pac-man/assists/images/profiles/profile5.jpg",
            "/home/hamezoua/pac-man/assists/images/profiles/profile7.png",
            "/home/hamezoua/pac-man/assists/images/profiles/profile8.jpeg",
            "/home/hamezoua/pac-man/assists/images/profiles/profile9.png",
            "/home/hamezoua/pac-man/assists/images/profiles/profile10.jpeg"
        ]
        for name, level in self.highscors.items():
            # border user info
            pygame.draw.rect(self.screen,
                             self.colors["yellow_dark"],
                             (self.width // 2 - 350, 100 + step, 900, 70),
                             border_radius=10)
            #ract to add user info
            pygame.draw.rect(self.screen,
                             self.colors["profile_bg"],
                             (self.width // 2 - 345, 102 + step, 890, 65),
                             border_radius=10)

            # rank number
            rank_surface = self.rank_font.render(f"{rank}", True,
                                                 self.colors["rank_number"])
            rank_rect = rank_surface.get_rect()
            rank_rect = (self.width // 2 - 325, 100 + step + 25)
            self.screen.blit(rank_surface, rank_rect)

            # profile image
            color_vip = self.colors["white"]
            if rank == 1:
                color_vip = self.colors["rank_1"]
            elif rank == 2:
                color_vip = self.colors["rank_2"]
            elif rank == 3:
                color_vip = self.colors["rank_3"]
            pygame.draw.rect(self.screen,
                             color_vip,
                             (self.width // 2 - 300, 100 + step + 10, 52, 52),
                             border_radius=7)
            profile = pygame.image.load(profiles[current_image])
            profile = pygame.transform.scale(profile, (45, 45)).convert()
            self.screen.blit(profile, (self.width // 2 - 297, 100 + step + 13))

            # add name
            name_surface = self.name_font.render(f"{name}", True,
                                                 self.colors["white"])
            name_rect = name_surface.get_rect()
            name_rect = (self.width // 2 - 240, 100 + step + 20)
            self.screen.blit(name_surface, name_rect)

            # add pts
            pts_surface = self.pts_font.render(f"{level} - PTS", True,
                                               self.colors["white"])
            pts_rect = pts_surface.get_rect()
            pts_rect = (self.width - 570, 100 + step + 21)
            self.screen.blit(pts_surface, pts_rect)
            step += 90
            rank += 1
            current_image = (current_image + 1) % len(profiles)

    def draw_back_button(self):
        pygame.draw.rect(self.screen, self.colors['yellow_dark'], (10, 20, 180, 50), border_radius=10)

        back_font = pygame.font.Font("./assists/fonts/PixeloidSansBold-1jpBg.ttf", 16)
        font_surface = back_font.render("BACK TO HOME", True, self.colors['deep_blue'])
        font_rect = font_surface.get_rect()
        font_rect= (10 + 18, 20 + 16)
        self.screen.blit(font_surface, font_rect)
        self.buttons.append(pygame.Rect((10, 20, 180, 50)))
    def draw_high_score(self):
        running = True
        while running:
            self.screen.fill(self.colors["dark"])
            self.screen.blit(self.background, (0, 0))
            self.draw_title()
            self.draw_profiles_place()
            self.draw_back_button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            if button.collidepoint(event.pos):
                                return 1
            pygame.display.update()
            pygame.time.wait(100)
