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

class HintRequest(BaseModel):
    game_id: str
    key: str
    hint_id: int  # เช่น 1, 2, 3
    
@app.post("/hint")
def get_hint(req: HintRequest):
    g=games.get(str(int(req.game_id)-1))
    game = games.get(req.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="ไม่พบเกมนี้")
    if req.game_id == "1":
        pass
    elif req.key != g.get("key"):
        raise HTTPException(status_code=401, detail="key ไม่ถูกต้อง")

    hint_key = f"hint{req.hint_id}"
    hint = game.get(hint_key)
    if not hint:
        raise HTTPException(status_code=404, detail="ไม่มี hint หมายเลขนี้")

    return {"hint": hint}


#-----------------------------------------------------------------------------------------------------------------
