from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os
from typing import Any
from game_in_and_out import games


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

class CheckRequest(BaseModel):
    items: Any  # รับได้ทุกชนิด: str, list, dict, int

class CheckResponse(BaseModel):
    correct: bool
    message: str

@app.post("/game/1/start", response_model=CheckResponse)
def check_answer(req: CheckRequest):
    game = games.get('1')
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    expected_output = game["output"]

    correct = req.items == expected_output

    return CheckResponse(
        correct=correct,
        message=f"✅ ถูกต้อง! \n key : {game['key']}" if correct else f"out: {req.items} \n ❌ ยังไม่ถูก ลองอีกครั้งนะ "
    )
    
@app.post("/game/2/ewadsdy", response_model=CheckResponse)
def check_answer(req: CheckRequest):
    game = games.get('2')
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    expected_output = game["output"]

    correct = req.items == expected_output

    return CheckResponse(
        correct=correct,
        message=f"✅ ถูกต้อง! \n key : {game['key']}" if correct else f"out: {req.items} \n ❌ ยังไม่ถูก ลองอีกครั้งนะ "
    )

@app.post("/game/3/fshtsjl", response_model=CheckResponse)
def check_answer(req: CheckRequest):
    game = games.get('3')
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    expected_output = game["output"]

    correct = req.items == expected_output

    return CheckResponse(
        correct=correct,
        message=f"✅ ถูกต้อง! \n key : {game['key']}" if correct else f"out: {req.items} \n ❌ ยังไม่ถูก ลองอีกครั้งนะ "
    )






#-----------------------------------------------------------------------------------------------------------------
