from pydantic import BaseModel, Field, ValidationError, model_validator

class level(BaseModel):
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

try:
    lelve1 = level(width=9,height=7, pacgum=45)
    print(lelve1.pacgum)
except ValidationError as e:
    for error in e.errors():
        e_key = error['loc']
        if e_key:
            pass
        else:
            msg = (error["msg"])
            print(msg)
