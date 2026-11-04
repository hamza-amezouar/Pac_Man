import sys
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.game_engine import Engine

def game_instruction(width: int, height: int, screen: pygame.surface.Surface, engine:"Engine"):
    run = True
    bg_image = pygame.image.load('assists/images/background.png')
    background = pygame.transform.scale(bg_image, (width, height))
    instra_img = pygame.image.load("assists/images/instraction.png")
    instruction = pygame.transform.scale(instra_img, (width*0.45, height*0.85))
    while run:
        screen.blit(background, (0,0))
        screen.blit(instruction, (width*0.29, height*0.05))
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
        
        pygame.display.update()
        