from src.engine.load_gifs import load_gif_frames
from src.models.maze import Maze_screen
import pygame


class Pacman_face(Maze_screen):

    def __init__(self, screen_w, screen_h, maze_w, maze_h, screen):
        super().__init__(screen_w, screen_h, maze_w, maze_h, screen)

        self.pacman_up = load_gif_frames("src/models/pacman_face/pacman/up.gif")
        self.pacman_down = load_gif_frames("src/models/pacman_face/pacman/down.gif")
        self.pacman_left = load_gif_frames("src/models/pacman_face/pacman/left.gif")
        self.pacman_right = load_gif_frames("src/models/pacman_face/pacman/right.gif")
        self.direction = "start"


    def draw_face(self, pacman_pos):
        pacman_size =  self.cell_size - 15
        if self.direction == "start":
            pacman_image = pygame.transform.scale(self.pacman_right[0],
                                                (pacman_size , pacman_size))
            self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
        elif self.direction == "up":
            # frames =  self.pacman_up
            pacman_image = pygame.transform.scale(self.pacman_up[0],
                                                            (pacman_size , pacman_size))
            self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))

        elif self.direction == "down":
            #frames = self.pacman_down
            pacman_image = pygame.transform.scale(self.pacman_down[0],
                                                                                    (pacman_size , pacman_size))
            self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
        elif self.direction == "left":
            #frames = self.pacman_left
            pacman_image = pygame.transform.scale(self.pacman_left[0],
                                                                                    (pacman_size , pacman_size))
            self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
        elif self.direction == "right":
            pacman_image = pygame.transform.scale(self.pacman_right[0],
                                                                        (pacman_size , pacman_size))
            self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
            #frames = self.pacman_right
        

    def moves_pacman(self, walls, pacman_pos, direction):
        current_x = (pacman_pos[0] - self.start_x) // self.cell_size
        current_y = (pacman_pos[1] - self.start_y) // self.cell_size

        if not (0 <= current_x < self.maze_w and  0 <= current_y < self.maze_h):
            return 

        if direction == "up":
            if current_y > 0 and not walls[current_y][current_x]['N']:
                pacman_pos[1] -= self.cell_size
        elif direction == "down":
            if current_y < self.maze_h - 1 and not walls[current_y][current_x]['S']:
                pacman_pos[1] += self.cell_size
        elif direction == "right":
            if current_x < self.maze_w - 1 and not walls[current_y][current_x]['E']:
                pacman_pos[0] += self.cell_size

        elif direction == "left":
            if current_x > 0 and not walls[current_y][current_x]['W']:
                pacman_pos[0] -= self.cell_size
        else:
            return
        self.direction = direction
        self.draw_face(pacman_pos)
        