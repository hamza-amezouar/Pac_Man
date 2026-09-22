from pydantic import BaseModel, Field, ValidationError, model_validator
from pathlib import Path
from typing import Dict, Union
import json

yellow = "\033[33m"
white = "\033[0m"
green = "\033[32m"
red = "\033[31m"

default_conf = {
    "highscore_filename": "highscore.json",
    "level": [{
        "width": 20,
        "height": 15,
        "pacgum": 42
    } for _ in range(10)],
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}


class Level(BaseModel):
    width: int = Field(ge=9)
    height: int = Field(ge=7)
    pacgum: int = Field(gt=0)

    @model_validator(mode="after")
    def check_pacgum_pacgum(self):
        if self.pacgum > (self.width * self.height) - 19:
            raise ValueError(f"pacgum={self.pacgum} is too large; "
                             f"maximum is {self.width * self.height - 19}")
        return self


class Validate(BaseModel):
    highscore_filename: str
    level: list[Level]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int = Field(gt=0)
    level_max_time: int = Field(gt=0)


class Parce:

    def extract_data(self, path: str) -> str | None:
        try:
            if Path(path).suffix != ".json":
                print(
                    f"{yellow}❌  Error: {path} is not a suffix '.json' file.{white}"
                )
                print(f"{green}->  Usage: python3 pac-man.py config.json{white}")
                exit(1)

            lines = []
            with open(path, "r") as f:
                for line in f:
                    if line.strip().startswith('#') or not line.strip():
                        continue
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    lines.append(line)
            return ("".join(lines))

        except FileNotFoundError:
            print(f"{red}❌  Error: {path} File not found{white}")
            print(f"{green}->  Usage: python3 pac-man.py config.json{white}")
            exit(1)

    def read_data(self, path: str) -> dict:

        try:
            parse_data = self.extract_data(path)

            if parse_data is None:
                print(f"{green}-> Using default: {default_conf}\n{white}")
                return default_conf

            data = json.loads(parse_data)

        except json.JSONDecodeError as e:
            print(f"{yellow}⚠️  Warning: is not valid JSON {e}{white}")
            print(f"{green}-> Using default: {default_conf}\n{white}")
            return default_conf

        except Exception as e:
            print(f"{yellow}⚠️  Warning: {e}{white}")
            print(f"{green}-> Using default: {default_conf}\n{white}")
            return default_conf

        return data

    def parse_data(self, path: str):
        try:
            data = self.read_data(path)

            if len(data["level"]) < 10:
                print(
                    f"{yellow}⚠️  Warning:  You entered {len(data['level'])} levels. "
                    f"The game must consist of at least 10 levels.{white}")
                print(
                    f"{green}-> Using default: {default_conf['level']}\n{white}"
                )

            data_valid = Validate(**data)
            return data_valid.model_dump()

        except ValidationError as e:
            for error in e.errors():
                e_key = (error["loc"][0])
                input = error["input"]
                msg = (error["msg"])
        
                if e_key in default_conf.keys():
                    print(
                        f"{yellow}⚠️  Warning: Your input {e_key}: {input} this {msg}{white}"
                    )
                    print(
                        f"{green}-> Using default: {default_conf[e_key]}\n{white}"
                    )
                    data[e_key] = default_conf[e_key]
                


            data_valid = Validate(**data)
        return data_valid.model_dump()
