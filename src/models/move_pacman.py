from src.engine.load_gifs import load_gif_frames
from src.models.maze import Maze_screen
import pygame


class Pacman_face(Maze_screen):

    def __init__(self, screen_w, screen_h, maze_w, maze_h, screen, data,engine, level):
        super().__init__(screen_w, screen_h, maze_w, maze_h, screen, data,engine, level)
        
        self.pacman_up = load_gif_frames("src/models/pacman_face/pacman/up.gif")
        self.pacman_down = load_gif_frames("src/models/pacman_face/pacman/down.gif")
        self.pacman_left = load_gif_frames("src/models/pacman_face/pacman/left.gif")
        self.pacman_right = load_gif_frames("src/models/pacman_face/pacman/right.gif")
        self.index = 0
        self.last_animation_time = 0
        self.animation_delay = 250
        self.frames = self.pacman_right


    def draw_face(self, pacman_pos, direction):
        pacman_size =  self.cell_size - 15
        current_time = pygame.time.get_ticks()
        if direction is None:
            self.frames = self.pacman_right
            self.index  = 0
        elif direction == "up":
            self.frames =  self.pacman_up
        elif direction == "down":
            self.frames = self.pacman_down
        elif direction == "left":
            self.frames = self.pacman_left
        elif direction == "right":
            self.frames = self.pacman_right
        elif direction == "blocked":
            self.index = 0

        if direction is not None and direction != "blocked":
            if current_time - self.last_animation_time >= self.animation_delay:
                self.index = (self.index + 1) % len(self.frames)
                self.last_animation_time = current_time
            

        pacman_image = pygame.transform.scale(self.frames[self.index],
                                                        (pacman_size , pacman_size))
        self.screen.blit(pacman_image, (pacman_pos[0] - pacman_size // 2,
        pacman_pos[1] - pacman_size // 2))
        

    def target_pacman(self,current_pos, direction, walls):
        c_x = int((current_pos[0] - self.start_x) // self.cell_size)
        c_y = int((current_pos[1] - self.start_y) // self.cell_size)
    
        if not (0 <= c_x < self.maze_w and  0 <= c_y < self.maze_h):
            return 
        if direction == "up":
            if not walls[c_y][c_x]['N']:
                target = (current_pos[0], current_pos[1] - self.cell_size)
                return target
            else:
                return None
        elif direction == "down":
            if not walls[c_y][c_x]['S']:
                return (current_pos[0], current_pos[1] + self.cell_size)
        elif direction == "left":
            if not walls[c_y][c_x]['W']:
                return (current_pos[0] - self.cell_size, current_pos[1])
        elif direction == "right":
            if not walls[c_y][c_x]['E']:
                return (current_pos[0] + self.cell_size, current_pos[1])
        return None

    def move_pacman(self,current_pos,target, speed):
        if target is None:
            return True
        if current_pos[1] > target[1]:
            current_pos[1] = max(
                target[1],
                current_pos[1] - speed
            )

        elif current_pos[1] < target[1]:
            current_pos[1] = min(
                target[1],
                current_pos[1] + speed
            )

        if current_pos[0] < target[0]:
            current_pos[0] = min(
                target[0],
                current_pos[0] + speed
            )

        elif current_pos[0] > target[0]:
            current_pos[0] = max(
                target[0],
                current_pos[0] - speed
            )

        return tuple(current_pos) == target
