from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from db_connection import session, engine
import database_model
from basemodel import PlayerCreate

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DB SESSION ------------------
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# ------------------ ADD PLAYER ------------------

@app.post("/add_player")
def add_player(player: PlayerCreate, db: Session = Depends(get_db)):

    new_player = database_model.Player(
        name=player.name,
        role=player.role,
        matches=player.matches,
        runs=player.runs,
        wickets=player.wickets,
        strike_rate=player.strike_rate,
        economy_rate=player.economy_rate,
        best_performance=player.best_performance
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return {"message": "✅ Player added"}
#------------------------------------------------------------------------
@app.put("/update_player/{player_id}")
def update_player(player_id: int, player: PlayerCreate, db: Session = Depends(get_db)):

    db_player = db.query(database_model.Player)\
                  .filter(database_model.Player.id == player_id)\
                  .first()

    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    db_player.name = player.name
    db_player.role = player.role
    db_player.matches = player.matches
    db_player.runs = player.runs
    db_player.wickets = player.wickets
    db_player.strike_rate = player.strike_rate
    db_player.economy_rate = player.economy_rate
    db_player.best_performance = player.best_performance

    db.commit()
    db.refresh(db_player)

    return {
        "message": "✅ Player updated successfully",
        "data": db_player
    }




# ------------------ GET ALL PLAYERS ------------------

@app.get("/get_players")
def get_players(db: Session = Depends(get_db)):
    return db.query(database_model.Player).all()


# ------------------ UPDATE PLAYER ------------------

@app.put("/update_player/{player_id}")
def update_player(player_id: int, player: PlayerCreate, db: Session = Depends(get_db)):

    existing_player = db.query(database_model.Player).filter(database_model.Player.id == player_id).first()

    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")

    existing_player.name = player.name
    existing_player.role = player.role
    existing_player.matches = player.matches
    existing_player.runs = player.runs
    existing_player.wickets = player.wickets
    existing_player.strike_rate = player.strike_rate
    existing_player.economy_rate = player.economy_rate
    existing_player.best_performance = player.best_performance

    db.commit()
    return {"message": "✅ Player Updated"}


# ------------------ DELETE PLAYER ------------------

@app.delete("/delete_player/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):

    player = db.query(database_model.Player).filter(database_model.Player.id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()
    return {"message": "✅ Player Deleted"}


# ------------------ TOP BATSMAN ------------------

@app.get("/top_batsman")
def top_batsman(db: Session = Depends(get_db)):
    player = db.query(database_model.Player).order_by(database_model.Player.runs.desc()).first()
    return player


# ------------------ TOP BOWLER ------------------

@app.get("/top_bowler")
def top_bowler(db: Session = Depends(get_db)):
    player = db.query(database_model.Player).order_by(database_model.Player.wickets.desc()).first()
    return player

# ------------------ PLAYER INSIGHTS (LEVEL 2) ------------------

@app.get("/player_insights/{player_id}")
def player_insights(player_id: int, db: Session = Depends(get_db)):

    p = db.query(database_model.Player).filter(database_model.Player.id == player_id).first()

    if not p:
        raise HTTPException(status_code=404, detail="Player not found")

    matches = p.matches if p.matches and p.matches > 0 else 1

    batting_score = (p.runs / matches)          # avg runs per match
    bowling_score = (p.wickets / matches)       # avg wickets per match

    # Simple normalized rating out of 10 (rule-based, not ML yet)
    overall_rating = batting_score / 10 + bowling_score * 2
    overall_rating = max(0, min(10, round(overall_rating, 2)))

    # Simple suggestion
    if batting_score >= 40 and p.role in ["Batsman", "All-rounder"]:
        suggestion = "Top-order batsman"
    elif bowling_score >= 1.5 and p.role in ["Bowler", "All-rounder"]:
        suggestion = "Strike bowler"
    else:
        suggestion = "Support / rotational player"

    return {
        "id": p.id,
        "name": p.name,
        "role": p.role,
        "matches": p.matches,
        "runs": p.runs,
        "wickets": p.wickets,
        "strike_rate": p.strike_rate,
        "economy_rate": p.economy_rate,
        "batting_score": round(batting_score, 2),
        "bowling_score": round(bowling_score, 2),
        "overall_rating": overall_rating,
        "suggested_role": suggestion
    }

# ------------------ BEST XI SUGGESTED TEAM (LEVEL 2/3) ------------------

@app.get("/best_xi")
def best_xi(db: Session = Depends(get_db)):

    players: List[database_model.Player] = db.query(database_model.Player).all()

    if not players:
        raise HTTPException(status_code=404, detail="No players in database")

    batsmen = [p for p in players if p.role == "Batsman"]
    bowlers = [p for p in players if p.role == "Bowler"]
    all_rounders = [p for p in players if p.role == "All-rounder"]

    # Sort each category
    batsmen = sorted(batsmen, key=lambda p: p.runs, reverse=True)
    bowlers = sorted(bowlers, key=lambda p: p.wickets, reverse=True)
    all_rounders = sorted(all_rounders, key=lambda p: (p.runs + p.wickets * 20), reverse=True)

    # Pick players (adjust if you have fewer)
    team = []
    team += batsmen[:4]        # 4 best batsmen
    team += bowlers[:4]        # 4 best bowlers
    team += all_rounders[:3]   # 3 best all-rounders

    # Remove duplicates (if a player appears twice somehow)
    seen = set()
    unique_team = []
    for p in team:
        if p.id not in seen:
            seen.add(p.id)
            unique_team.append(p)

    # Convert to simple dicts
    result = [
        {
            "id": p.id,
            "name": p.name,
            "role": p.role,
            "matches": p.matches,
            "runs": p.runs,
            "wickets": p.wickets,
            "strike_rate": p.strike_rate,
            "economy_rate": p.economy_rate,
        }
        for p in unique_team
    ]

    return {
        "team_size": len(result),
        "players": result
    }
