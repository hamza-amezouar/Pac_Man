import sys

from src.engine.game_engine import Engine

if __name__ == "__main__":
    try:
        game = Engine(1920, 1080)
        game.run_engine()
    except KeyboardInterrupt as e:
        print(e)
        sys.exit(1)
