from pydantic import BaseModel

class PlayerCreate(BaseModel):
    name: str
    role: str
    matches: int
    runs: int
    wickets: int
    strike_rate: float
    economy_rate: float
    best_performance: str
