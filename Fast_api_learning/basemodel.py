from pydantic import BaseModel, Field

class Cricket(BaseModel):
    name:str = Field(..., min_length=3, max_length=20)
    age:int = Field(..., ge=10, le=60)
    score:int = Field(..., ge=0, le=200)

class Ipl(BaseModel):
    name:str
    age:int
    score:int