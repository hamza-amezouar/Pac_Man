from pydantic import BaseModel, Field, ValidationError, model_validator
from pathlib import Path
from typing import Dict, Any
import json

yellow = "\033[33m"
white = "\033[0m"
green = "\033[32m"
red = "\033[31m"

default_conf: Dict[str, Any] = {
    "highscore_filename": "highscore.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "level": [{
        "width": 20,
        "height": 15,
        "pacgum": 42
    } for _ in range(10)]
}


class Level(BaseModel):
    """
    store and validate the settings of one game level

    Attributes:
        width: the width of the level
        height: the height of the level
        pacgum: the number of pacgum in the level
    """

    width: int = Field(ge=9)
    height: int = Field(ge=7)
    pacgum: int = Field(gt=0)

    @model_validator(mode="after")
    def check_pacgum_pacgum(self) -> "Level":
        """
        Check that the number of pacgum fits in the level

        Returns:
            the validated level

        Raises:
            ValueError: If there are too many pac-gums.
        """

        if self.pacgum > (self.width * self.height) - 19:
            raise ValueError(f"pacgum={self.pacgum} is too large; "
                             f"maximum is {self.width * self.height - 19}")
        return self


class Validate(BaseModel):
    """
    Store and validate the main game configuration.

    Attributes:
        highscore_filename: The name of the high-score file.
        lives: The number of lives for the player.
        pacgum: The number of pac-gums in the game.
        points_per_pacgum: The points given for one pac-gum.
        points_per_super_pacgum: The points given for one super pac-gum.
        points_per_ghost: The points given for one ghost.
        seed: The seed used to create random values.
        level_max_time: The maximum time allowed for one level.
        level: The list of game levels. It must contain at least 10 levels.
    """
    highscore_filename: str
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int = Field(gt=0)
    level_max_time: int = Field(gt=0)
    level: list[Level] = Field(min_length=10)


class Parce:
    """
    Read, clean, validate, and prepare the game configuration.
    This class reads the JSON configuration file, removes comments,
    adds missing default values, and validates the configuration.
    """

    def extract_data(self, path: str) -> str:
        """
        Read a JSON configuration file and remove comments and empty lines.
        Args:
            path: Path to the JSON configuration file.

        Returns:
            The configuration file content as a string without comments
            or empty lines.

        Raises:
            SystemExit: If the file does not have a '.json' extension
                or cannot be found.
        """
        try:
            if Path(path).suffix != ".json":
                print(f"{yellow}❌  Error: {path} is not a suffix"
                      f" '.json' file.{white}")
                print(
                    f"{green}->  Usage: python3 pac-man.py config.json{white}")
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

    def read_data(self, path: str) -> Dict[str, Any]:
        """
        Read and parse the configuration file.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            The configuration data as a dictionary. Default configuration
            is returned when the JSON data is invalid.
        """

        try:
            parse_data = self.extract_data(path)
            data: Dict[str, Any] = json.loads(parse_data)

        except json.JSONDecodeError as e:
            print(f"{yellow}⚠️  Warning: is not valid JSON {e}{white}")
            print(f"{green}-> Using default: {default_conf}\n{white}")
            return default_conf

        except Exception as e:
            print(f"{yellow}⚠️  Warning: {e}{white}")
            print(f"{green}-> Using default: {default_conf}\n{white}")
            return default_conf

        return data

    def check_levels(self, i: int, level: Dict[str, Any],
                     data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate one level and replace invalid values with defaults.

        Args:
            i: Index of the level in the configuration.
            level: Configuration data for one level.
            data: Complete configuration data.

        Returns:
            The validated level as a dictionary.
        """
        try:
            parce_level = Level(**level)

        except ValidationError as e:
            for error in e.errors():
                input_value = error["input"]
                msg = error["msg"]

                if not error['loc']:
                    e_key = "pacgum"
                else:
                    e_key = str(error["loc"][0])

                print(f"{yellow}⚠️  Warning: Level {i + 1}: {msg}\n"
                      f"   Your input: {input_value }\n"
                      f"   Invalid configuration for '{e_key}{white}'\n"
                      f"{green}→  Using default value: "
                      f"{e_key}={default_conf['level'][i][e_key]}\n{white}")
                data['level'][i][e_key] = default_conf["level"][i][e_key]

            parce_level = Level(**level)

        return parce_level.model_dump()

    def parse_data(self, path: str) -> Dict[str, Any]:
        """
        Parse, validate, and prepare the complete configuration.
        Missing levels are added from the default configuration.
        Invalid levels or values are replaced with safe default values.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            The validated configuration as a dictionary.
        """

        try:
            data = self.read_data(path)

            if "level" not in data:
                print(
                    f"{yellow}⚠️  Warning: 'level' is missing.{white}"
                )
                print(
                    f"{green}-> Using default levels: "
                    f"{default_conf['level']}\n{white}"
                )
                data["level"] = default_conf["level"]

            if not isinstance(data["level"], list) or not data['level']:
                print(f"{yellow}⚠️  Warning: 'level' must be a"
                      f" non-empty list {white}")
                print(f"{green}-> Using default: {default_conf['level']}"
                      f"\n{white}")
                data["level"] = default_conf['level']

            elif len(data["level"]) < 10:
                print(f"{yellow}⚠️  Warning: You provided only "
                      f"{len(data['level'])} levels. "
                      f"The game must consist of at least 10 levels.{white}")

                missing_levels = 10 - len(data["level"])
                default_level = default_conf["level"][:missing_levels]

                print(f"{green}-> Adding {missing_levels}"
                      " default level(s)"
                      f"{default_level}{white}\n")

                data["level"] += default_level

            for i in range(len(data["level"])):
                if not isinstance(data['level'][i], dict):
                    print(f"{yellow}⚠️  Warning: Your Level {i + 1}"
                          f" is Invalid.{white}")
                    print(f"{green}-> Adding default level"
                          f"{default_conf['level'][i]}\n{white}")
                    data["level"][i] = default_conf["level"][i]

                self.check_levels(i, data["level"][i], data)
            data_valid = Validate(**data)

            return data_valid.model_dump()

        except ValidationError as e:
            for error in e.errors():
                e_key = error["loc"][0]
                input_value = error["input"]
                msg = error["msg"]
                e_type = error['type']

                if e_key in default_conf.keys():
                    print(f"{yellow}⚠️  Warning: {e_type}: {msg}\n"
                          f"   - Your input: {input_value}\n"
                          f"   - Invalid configuration for '{e_key}{white}'\n")
                    print(f"{green}-> Using default:{e_key}="
                          f"{default_conf[e_key]}\n{white}")
                    data[e_key] = default_conf[e_key]

            data_valid = Validate(**data)

        return data_valid.model_dump()
