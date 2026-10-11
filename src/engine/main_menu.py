from typing import Dict, Tuple

import pygame


class Draw_main:
    """
    Manages the main menu display,
    transition animations, and button interactions.
    Handles menu rendering, hover effects, and click event navigation.
    """

    def __init__(self, WIDTH: int, HEIGHT: int, screen: pygame.surface.Surface,
                 colors: Dict[str, Tuple[int, int, int]]):
        """
        Initializes screen bounds,
        background images, custom fonts, and button lists.
        """
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = screen
        self.colors = colors
        self.bg_image: pygame.surface.Surface = pygame.image.load(
            './assists/images/background.png')
        self.background: pygame.surface.Surface = pygame.transform.scale(
            self.bg_image, (self.width, self.height)).convert()
        self.menu_font: pygame.font.Font = pygame.font.Font(
            "./assists/fonts/PixeloidSansBold-1jpBg.ttf", 30)
        self.buttons: list[pygame.rect.Rect] = []

    def Draw_animation(self, step: int) -> bool:
        """
        Renders a sliding curtain animation
        opening from the center outward.
        Returns True when the curtain
        fully clears the screen bounds, else False.
        """
        start = self.width // 2
        if start + step >= self.width:
            return True
        pygame.draw.rect(self.screen, self.colors["blue_light"],
                         (start + step, 0, start, self.height))
        pygame.draw.rect(self.screen, self.colors["blue_light"],
                         (0 - step, 0, start, self.height))
        return False

    def init_buttons(self) -> None:
        """
        Creates and appends rectangular collision
        bounding boxes for menu buttons.
        """
        center_x = self.width // 2
        center_y = self.height // 2
        self.buttons.append(
            pygame.Rect(center_x - 150, center_y - 200, 400, 60))
        self.buttons.append(
            pygame.Rect(center_x - 150, center_y - 100, 400, 60))
        self.buttons.append(pygame.Rect(center_x - 150, center_y, 400, 60))
        self.buttons.append(
            pygame.Rect(center_x - 150, center_y + 100, 400, 60))

    def Draw_buttons_menu(self, mouse: tuple[int, int]) -> None:
        """
        Renders interactive menu buttons,
        updating visual feedback and cursor style
        based on mouse hover state before rendering text
        labels on each button.
        """
        center_x = self.width // 2
        center_y = self.height // 2
        if mouse != (0, 0):
            is_hover = False
            for button in self.buttons:
                if button.collidepoint(mouse):
                    is_hover = True
                    pygame.draw.rect(self.screen,
                                     self.colors['yellow_dark'],
                                     button,
                                     border_radius=20)
                else:
                    pygame.draw.rect(self.screen,
                                     self.colors['yellow'],
                                     button,
                                     border_radius=10)
            if is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            for button in self.buttons:
                pygame.draw.rect(self.screen,
                                 self.colors['yellow'],
                                 button,
                                 border_radius=10)

        start_game_font: pygame.surface.Surface = self.menu_font.render(
            "START GAME", True, self.colors['deep_blue'])
        start_game_rect: pygame.rect.Rect = start_game_font.get_rect()
        start_game_rect.center = (center_x - 150 + 400 // 2,
                                  center_y - 200 + 60 // 2)
        self.screen.blit(start_game_font, start_game_rect)

        high_score_font: pygame.surface.Surface = self.menu_font.render(
            "VIEW HIGHSCORES", True, self.colors['deep_blue'])
        high_score_rect: pygame.rect.Rect = high_score_font.get_rect()
        high_score_rect.center = (center_x - 150 + 400 // 2,
                                  center_y - 100 + 60 // 2)
        self.screen.blit(high_score_font, high_score_rect)

        instructions_font: pygame.surface.Surface = self.menu_font.render(
            "INSTRUCTIONS", True, self.colors['deep_blue'])
        instructions_rect: pygame.rect.Rect = instructions_font.get_rect()
        instructions_rect.center = (center_x - 150 + 400 // 2,
                                    center_y + 60 // 2)
        self.screen.blit(instructions_font, instructions_rect)

        exit_font: pygame.surface.Surface = self.menu_font.render(
            "EXIT", True, self.colors['deep_blue'])
        exit_rect: pygame.rect.Rect = exit_font.get_rect()
        exit_rect.center = (center_x - 150 + 400 // 2,
                            center_y + 100 + 60 // 2)
        self.screen.blit(exit_font, exit_rect)

    def Draw_menu(self) -> int:
        """
        Runs the main menu loop: plays the opening transition animation first,
        then handles user input, button interactions, and display updates.
        """
        step = 0
        x = 0
        self.init_buttons()
        while x < 35:
            pygame.time.wait(10)
            self.screen.fill(self.colors["dark"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3
            self.screen.blit(self.background, (0, 0))
            self.Draw_buttons_menu((0, 0))
            self.Draw_animation(step)
            step += 25
            pygame.display.update()
            x += 1
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(self.colors["dark"])
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            if button.collidepoint(event.pos):
                                if button == self.buttons[0]:
                                    return 0
                                if button == self.buttons[1]:
                                    return 1
                                if button == self.buttons[3]:
                                    return 3
            self.Draw_buttons_menu(mouse_pos)
            pygame.display.update()
