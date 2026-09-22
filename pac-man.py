from src.config_parser import Parce, green, white, red
import sys
import json


def get_data() -> dict:
    p = Parce()

    if len(sys.argv) <= 1:
        print(f"❌  {red}Error: Configuration file is required{white}")
        print(f"{green}->  Usage: python3 pac-man.py config.json{white}")
        exit(1)

    else:
        data = p.parse_data(sys.argv[1])

    return data


if __name__ == "__main__":
    data = get_data()
    print(data)
    with open("result.json", 'w') as f:
        json.dump(data, f, indent=2)
    print("next")
