from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os

from game_data import games
from models import PuzzleResponse, AnswerRequest, AnswerResponse, HintResponse
from logic import check_answer

app = FastAPI()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือ ["*"] เพื่อให้ทุก origin เข้าถึงได้ (ใช้เฉพาะช่วง dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#-----------------------------------------------------------------------------------------------------------------
@app.get("/")
def home():
    return "test api python"
#-----------------------------------------------------------------------------------------------------------------
@app.get("/game/{game_id}", response_model=PuzzleResponse)
def get_game(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return PuzzleResponse(
        id=game["id"],
        title=game["title"],
        description=game["description"],
        input=game["input"]
    )

@app.get("/game/{game_id}/hint", response_model=HintResponse)
def get_hint(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return HintResponse(hint=game["hint"])

@app.post("/game/{game_id}/check", response_model=AnswerResponse)
def check(game_id: str, req: AnswerRequest):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    correct = check_answer(req.code, game["expected_output"])
    return AnswerResponse(
        correct=correct,
        message="✅ ถูกต้อง!" if correct else "❌ ยังไม่ถูก ลองอีกครั้งนะ"
    )
