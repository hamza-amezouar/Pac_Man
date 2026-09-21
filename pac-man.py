from src.config_parser import Parce
import sys
import json 

def get_data()-> dict:
    p = Parce()

    if len(sys.argv) <= 1:
        print(f"⚠️  Warning: missing file 'config.json'")
        data = p.parse_data("config.json")

    else:
        data = p.parse_data(sys.argv[1])

    return data


if __name__ == "__main__":
    data = get_data()
    print(data)
    with open("result.json",'w') as f:
        json.dump(data,f, indent=2)
    print("next")
