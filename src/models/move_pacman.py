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
        self.index = 0


    def draw_face(self, pacman_pos):
        frames = self.pacman_right
        pacman_size =  self.cell_size - 15
        # current_time = pygame.time.get_ticks()
        if self.direction == "start":
            frames = self.pacman_right
            index  = 0
        elif self.direction == "up":
            frames =  self.pacman_up
        elif self.direction == "down":
            frames = self.pacman_down
        elif self.direction == "left":
            frames = self.pacman_left
        elif self.direction == "right":
            frames = self.pacman_right
        if self.direction != "start":
            index = (self.index + 1) % len(frames)
        pacman_image = pygame.transform.scale(frames[0],
                                                        (pacman_size , pacman_size))
        self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
        self.index = (self.index + 1) % len(frames)
        

    def target_pacman(self,pacman_pos, direction):
        c_x = (pacman_pos[0] - self.start_x) // self.cell_size
        c_y = (pacman_pos[1] - self.start_y) // self.cell_size
        speed = 2
        if not (0 <= c_x < self.maze_w and  0 <= c_y < self.maze_h):
            return 
        if direction == "up":
            if c_y > 0:
                target_y = pacman_pos[1] - self.cell_size
                return(pacman_pos[0], target_y)
        elif direction == "right":
            if c_x < self.maze_w - 1:
                target_x = pacman_pos[0] + self.cell_size
                return (target_x, pacman_pos[1])
        return None


    def move_pacman(self, walls, pacman_pos, direction, target):
        speed = 2
        c_x = (pacman_pos[0] - self.start_x) // self.cell_size
        c_y = (pacman_pos[1] - self.start_y) // self.cell_size
        t_x = (target[0] - self.start_x) // self.cell_size
        t_y = (target[1] - self.start_y) // self.cell_size
        if direction == "up":
            pygame.draw.circle(self.screen, (255,255,255), (target[0], target[1]), 20)
            if pacman_pos[1] <= target[1]:
                pacman_pos[1] = target[1]
                print(pacman_pos[1], target[1])
                return
            if c_y > 0 and not walls[t_y][t_x]["S"]:
                pacman_pos[1] -= speed

                
        elif direction == "right":  
            pygame.draw.circle(self.screen, (255,255,255), (target[0], target[1]), 20)
            if pacman_pos[0] >= target[0]:
                pacman_pos[0] = target[0]
                return
            if c_x < self.maze_w - 1 and not walls[t_y][t_x]['W']:
                pacman_pos[0] += speed
        


        # else:
        #     return
        # self.direction = direction
        # self.draw_face(pacman_pos)
        