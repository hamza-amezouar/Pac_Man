import sys
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.game_engine import Engine


def game_instruction(width: int, height: int, screen: pygame.surface.Surface,
                     engine: "Engine") -> int:
    """
    Display the game instructions and handle user input.

    Args:
        width: Width of the game window.
        height: Height of the game window.
        screen: Pygame surface used to display the instructions.
        engine: Game engine used to access the back button.

    Returns:
        0 if the user clicks the back button.
        -1 if the instruction screen is closed normally.
    """
    run = True
    bg_image = pygame.image.load('assists/images/background.png')
    background = pygame.transform.scale(bg_image, (width, height))
    instra_img = pygame.image.load("assists/images/instraction.png")
    instruction = pygame.transform.scale(instra_img,
                                         (width * 0.40, height * 0.90))
    arrow_keys_img = pygame.image.load("assists/images/keys.png")
    arrow_keys = pygame.transform.scale(arrow_keys_img,
                                        (width * 0.10, height * 0.10))
    controls_img = pygame.image.load("assists/images/controls.png")
    controls = pygame.transform.scale(controls_img,
                                      (width * 0.08, height * 0.07))
    p_cheat_img = pygame.image.load("assists/images/p_cheat.png")
    p_cheat = pygame.transform.scale(p_cheat_img,
                                     (width * 0.05, height * 0.06))
    titles_font = pygame.font.Font("assists/fonts/PixeloidMono-nAOpP.ttf", 35)
    source_font = pygame.font.Font(None, 30)
    while run:
        screen.blit(background, (0, 0))
        screen.blit(instruction, (width * 0.29, height * 0.01))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if pygame.K_q:
                    sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in engine.draw_highscore.buttons:
                        if button.collidepoint(event.pos):
                            return 0
        mouse_pos = pygame.mouse.get_pos()
        engine.draw_highscore.draw_back_button(mouse_pos, "BACK TO HOME")
        padding = 0
        source_size = 0
        source_x = width * 0.33
        source_y = height * 0.25 + padding + 50
        for t in range(3):
            title_y = height * 0.25 + padding
            title_x = width * 0.35

            if t == 0:
                title = "*HOW TO PLAY"
                source = ("- Use the arrow keys or AWDS to move Pac-Man.\n"
                          "- Eat all the pac-dots to complete the level.\n"
                          "- Collect power pellets to scare ghosts.\n"
                          "- Avoid ghosts or you will lose a life.\n"
                          "- Complete the maze before time runs out.\n")
            if t == 1:
                title = "*CONTROLS"
                source = ("- ARROW KEYS / WASD — Move Pac-Man.\n"
                          "- SPACE — Pause the game\n"
                          "- Q — Quit the game\n")
                screen.blit(arrow_keys, (source_x + 310, source_y + 245))
                screen.blit(controls, (source_x + 150, source_y + 270))
            if t == 2:
                title = "*CHEAT MODE"
                source = (
                    "- Level skip (immediately win the current level).\n")
                screen.blit(p_cheat, ((source_x + source_size + 75,
                                       source_y + source_size - 20)))

            lines = source.split('\n')
            for i, line in enumerate(lines):
                text = source_font.render(line, True, (10, 0, 0))
                screen.blit(text, (source_x, source_y + source_size + 30 * i))
            titles = titles_font.render(title, True, (90, 20, 10))
            screen.blit(titles, (title_x, title_y))
            padding += 200
            source_size += 200

        pygame.display.update()
    return -1
