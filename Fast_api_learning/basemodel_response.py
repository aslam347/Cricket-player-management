from pydantic import BaseModel


class Average(BaseModel):
    name:str
    average:float
