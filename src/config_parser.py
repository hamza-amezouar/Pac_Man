from pydantic import BaseModel, Field, ValidationError, model_validator
from pathlib import Path
from typing import Dict, Union
import json

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


class level(BaseModel):
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
    level: list
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
                print(f"⚠️  Warning: {path} is not a suffix '.json' file.")
                return None

            lines = []
            with open(path, "r") as f:
                for line in f:
                    if line.strip().startswith('#') or not line.strip():
                        continue
                    lines.append(line)
            return ("".join(lines))

        except FileNotFoundError as e:
            print(f"⚠️  Warning: {path} File not found {e}")
            return None

    def read_data(self, path: str) -> dict:

        try:
            parse_data = self.extract_data(path)

            if parse_data is None:
                return default_conf

            data = json.loads(parse_data)

        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: is not valid JSON {e}")
            return default_conf

        except Exception as e:
            print(f"⚠️  Warning: {e}")
            return default_conf

        return data

    def parse_data(self, path: str):
        try:
            data = self.read_data(path)
            data_valid = Validate(**data)
            return data_valid.model_dump()

        except ValidationError as e:
            for error in e.errors():
                e_key = (error["loc"][0])
                input = error["input"]
                msg = (error["msg"])

                if e_key in default_conf.keys():
                    print(
                        f"⚠️  Warning: Your input {e_key}: {input} this {msg}")
                    print(f"-> Using default: {default_conf[e_key]}\n")
                    data[e_key] = default_conf[e_key]

            data_valid = Validate(**data)
        return data_valid.model_dump()
