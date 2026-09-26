from src.config_parser import Parce
from src.engine.game_engine import Engine

if __name__ == "__main__":
    p = Parce()
    data = p.get_data()
    print(data)
    engine = Engine(1920, 1080)
    engine.run_engine()
