from pydantic import BaseModel

class AnswerRequest(BaseModel):
    code: str

class AnswerResponse(BaseModel):
    correct: bool
    message: str

class HintResponse(BaseModel):
    hint: str

class PuzzleResponse(BaseModel):
    id: str
    title: str
    description: str
    input: str
