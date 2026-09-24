import pygame
import time



class Draw_main:
    def __init__(self, WIDTH, HEIGHT, screen, colors):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.colors = colors
        self.bg_image = pygame.image.load('./assists/images/background.png')
        self.background = pygame.transform.scale(self.bg_image, (1920, 1080)).convert()
        self.menu_font = pygame.font.Font("./assists/fonts/PixeloidSansBold-1jpBg.ttf", 30)
        self.buttons = []
    def Draw_animation(self, step):
        start = self.width // 2
        if start + step >= self.width:
            return True
        pygame.draw.rect(self.screen, self.colors["deep_blue"], (start + step, 0, start, self.height))
        pygame.draw.rect(self.screen, self.colors["deep_blue"], (0 - step, 0, start, self.height))
        return False


    def init_buttons(self):
        center_x = self.width // 2
        center_y = self.height // 2
        self.buttons.append(pygame.Rect(center_x - 150, center_y - 200, 400, 60))
        self.buttons.append(pygame.Rect(center_x - 150, center_y - 100, 400, 60))
        self.buttons.append(pygame.Rect(center_x - 150, center_y, 400, 60))
        self.buttons.append(pygame.Rect(center_x - 150, center_y + 100, 400, 60))

    def Draw_buttons_menu(self):

        center_x = self.width // 2
        center_y = self.height // 2
        pygame.draw.rect(self.screen, self.colors['yellow'], (center_x - 150, center_y - 200, 400, 60), border_radius=10)
        pygame.draw.rect(self.screen, self.colors['yellow'], (center_x - 150, center_y - 200, 400, 60))

        pygame.draw.rect(self.screen, self.colors['yellow'], (center_x - 150, center_y - 100, 400, 60), border_radius=10)

        pygame.draw.rect(self.screen, self.colors['yellow'], (center_x - 150, center_y, 400, 60), border_radius=10)

        pygame.draw.rect(self.screen, self.colors['yellow'], (center_x - 150, center_y + 100, 400, 60), border_radius=10)

        start_game_font = self.menu_font.render("START GAME", True, self.colors['buttons'])
        start_game_rect = start_game_font.get_rect()
        start_game_rect.center = (center_x - 150 + 400 // 2, center_y - 200 + 60 // 2)
        self.screen.blit(start_game_font, start_game_rect)

        high_score_font = self.menu_font.render("VIEW HIGHSCORES", True, self.colors['buttons'])
        high_score_rect = high_score_font.get_rect()
        high_score_rect.center = (center_x - 150 + 400 // 2, center_y - 100 + 60 // 2)
        self.screen.blit(high_score_font, high_score_rect)

        instructions_font = self.menu_font.render("INSTRUCTIONS", True, self.colors['buttons'])
        instructions_rect = instructions_font.get_rect()
        instructions_rect.center = (center_x - 150 + 400 // 2, center_y + 60 // 2)
        self.screen.blit(instructions_font, instructions_rect)

        exit_font = self.menu_font.render("EXIT", True, self.colors['buttons'])
        exit_rect = exit_font.get_rect()
        exit_rect.center = (center_x - 150 + 400 // 2, center_y + 100 + 60 // 2)
        self.screen.blit(exit_font, exit_rect)

    def Draw_menu(self):
        step = 0
        x = 0
        while True:
            pygame.time.wait(10)
            self.screen.fill(self.colors["dark"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.blit(self.background,(0, 0))
            self.Draw_buttons_menu()
            self.Draw_animation(step)
            step += 25
            pygame.display.update()
            if x == 35:
                break
            x += 1
        self.init_buttons()
        while True:
            self.screen.fill(self.colors["dark"])
            self.screen.blit(self.background,(0, 0))
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.Draw_buttons_menu()
            pygame.display.update()
            