# from fastapi import FastAPI
# from basemodel import Cricket, Ipl
# from basemodel_response import Average
# from dependence import dependency
# from fastapi import Depends
# from fastapi.middleware.cors import CORSMiddleware
# from db_connection import session, engine
# import database_model
#
# app = FastAPI()
#
# database_model.Base.metadata.create_all(bind=engine)
#
# #
#
# origins = [
#    "http://192.168.211.:8000",
#    "http://localhost",
#    "http://localhost:8080",
# ]
# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
# )
#
#
# score_data = []
#
# def init_db():
#     db = session()
#
#     for scored_data in score_data:
#         db.add(database_model.Ipl(**scored_data.model_dump()))
#
#     db.commit()
#     init_db()
#
#
#
# @app.post("/player")
# def player(cricket:Cricket) :
#     return f"The Player {cricket.name},and their {cricket.age}, and he got {cricket.score} today"
#
#
#
#
# @app.post("/player_average", response_model=Average)
# def player_average(cricket: Cricket):
#     # compute any average logic you want
#     average_value = cricket.score * 100 / 2   # your formula
#     return {"name": cricket.name, "average": average_value}
#
# # dependency Injection code to reuse same again and again (I create file to handle this)
# @app.get("/user/")
# async def user(dep: dict = Depends(dependency)):
#     return dep
#
# @app.post("/ipl_data")
# def ipl_data(ipl:Ipl):
#     score_data.append(ipl.model_dump())
#     return f"score data stored Successfully and their details{score_data}"
#
# @app.get("/get_IplData")
# def get_IplData():
#     db = session()
#     db.query()
#     return score_data
#
#
# @app.put("/update_iplData/{name}")
# def update_iplData(name: str, ipl: Ipl):
#     for index, player in enumerate(score_data):
#         if player["name"] == name:
#             score_data[index] = ipl.model_dump()
#             return {"message": "Player updated successfully", "data": score_data[index]}
#
#     return {"error": "Player not found"}
#
#
# @app.delete("/delete_iplData/{name}")
# def delete_iplData(name: str):
#     for index, player in enumerate(score_data):
#         if player["name"] == name:
#             removed_player = score_data.pop(index)
#             return {
#                 "message": "Player deleted successfully",
#                 "deleted_player": removed_player
#             }
#
#     return {"error": "Player not found"}


from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from basemodel import Cricket, Ipl
from basemodel_response import Average
from dependence import dependency
from db_connection import session, engine
import database_model

app = FastAPI()

# Create tables in database
database_model.Base.metadata.create_all(bind=engine)

# -------------------- CORS --------------------

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- BASIC APIs --------------------

@app.post("/player")
def player(cricket: Cricket):
    return f"The Player {cricket.name}, their age is {cricket.age}, and he got {cricket.score} today"


@app.post("/player_average", response_model=Average)
def player_average(cricket: Cricket):
    average_value = cricket.score * 100 / 2
    return {"name": cricket.name, "average": average_value}


@app.get("/user/")
async def user(dep: dict = Depends(dependency)):
    return dep


# -------------------- DATABASE SESSION --------------------

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# -------------------- CREATE (POST) --------------------

@app.post("/ipl_data")
def ipl_data(ipl: Ipl, db: Session = Depends(get_db)):

    new_player = database_model.Ipl(
        name=ipl.name,
        age=ipl.age,
        score=ipl.score
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return {
        "message": "Data saved in MySQL successfully",
        "data": {
            "id": new_player.id,
            "name": new_player.name,
            "age": new_player.age,
            "score": new_player.score
        }
    }


# -------------------- READ (GET) --------------------

@app.get("/get_IplData")
def get_IplData(db: Session = Depends(get_db)):
    data = db.query(database_model.Ipl).all()
    return data


# -------------------- UPDATE --------------------

@app.put("/update_iplData/{player_id}")
def update_iplData(player_id: int, ipl: Ipl, db: Session = Depends(get_db)):

    player = db.query(database_model.Ipl).filter(database_model.Ipl.id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.name = ipl.name
    player.age = ipl.age
    player.score = ipl.score

    db.commit()
    db.refresh(player)

    return {
        "message": "Player updated successfully",
        "data": player
    }


# -------------------- DELETE --------------------

@app.delete("/delete_iplData/{player_id}")
def delete_iplData(player_id: int, db: Session = Depends(get_db)):

    player = db.query(database_model.Ipl).filter(database_model.Ipl.id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()

    return {"message": "Player deleted successfully"}
