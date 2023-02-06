from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Game(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=0, max_length=250)
    rating: float = Field(gt=-1, lt=11) 

@app.get('/')
def get_games(db: Session = Depends(get_db)):
    return db.query(models.Games).all()

@app.post('/')
def add_game(game: Game, db: Session = Depends(get_db)):
    game_model = models.Games()

    game_model.title = game.title
    game_model.author = game.author
    game_model.genre = game.genre
    game_model.description = game.description
    game_model.rating = game.rating

    db.add(game_model)
    db.commit()

    return game

@app.put('/')
def edit_game(game_id: int, game: Game, db: Session = Depends(get_db)):
    game_model = db.query(models.Games).filter(models.Games.id == game_id).first()

    if game_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game ID {game_id}: is not found"
        )
    
    game_model.title = game.title
    game_model.author = game.author
    game_model.genre = game.genre
    game_model.description = game.description
    game_model.rating = game.rating

    db.add(game_model)
    db.commit()

    return game

@app.delete('/')
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game_model = db.query(models.Games).filter(models.Games.id == game_id).first()

    if game_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Game ID {game_id}: is not found"
        )
    
    db.query(models.Games).filter(models.Games.id == game_id).delete()
    db.commit()

    return f"Game ID {game_id} delete"