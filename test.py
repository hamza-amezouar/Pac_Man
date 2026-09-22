from pydantic import BaseModel, Field, ValidationError, model_validator
from src.config_parser import default_conf
import json

class Level(BaseModel):
    width:int = Field(ge=9)
    height:int = Field(ge=7)
    pacgum:int = Field(gt=0)

    @model_validator(mode="after")
    def check_pacgum_pacgum(self):
        if self.pacgum > (self.width * self.height) - 19:
            raise ValueError(
    f"pacgum={self.pacgum} is too large; "
    f"maximum is {self.width * self.height - 19}"
)
        return self

class Validate(BaseModel):
    levels: list[Level]
    lives:int 


if __name__=="__main__":
        data = {
            "lives":3,    
            "levels": [
                {
                    "width": 21,
                    "height": 14,
                    "pacgum": -45
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 10,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 10,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                },
                {
                    "width": 20,
                    "height": 15,
                    "pacgum": 42
                }
            ]
        }

def cheks_level(i, l):
    try:
        level_parrce = Level(**l)
    except ValidationError as e :
        for error in e.errors():
            e_key = error["loc"][0]
            input = error['input']
            type = error['type']
            msg = error['msg']
            print(f"⚠️ Warning: Level {i} your {input}")
            print(e_key, input, type, msg)

            data["levels"][i][e_key] = default_conf["level"][i][e_key] 

    level_parrce = Level(**data["levels"][i])
    return level_parrce.model_dump()



levels = []
for i in  range(len(data['levels'])):
    level = cheks_level(i, data["levels"][i])
    levels.append(level)
with open("res.json", "w") as f:
    json.dump(levels, f, indent=2)
    

# print(data['levels'][1].keys)