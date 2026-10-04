from src.config_parser import Parse
from src.models.maze import Maze, Screen
from src.models.move_pacman import Pacman_face
from src.models.main import maze_loop


if __name__ == "__main__":

    parse = Parse()
    data = parse.get_data()
    width = data['level'][0]['width']
    height = data['level'][0]['height']
    d_seed = data['seed']

    maze1 = Maze(size=(width, height), seed=55, level=2)
    walls = maze1.get_walls()
    screen = Screen(width, height)
    pacman = Pacman_face(width, height)
    maze_loop(screen, walls, pacman)

