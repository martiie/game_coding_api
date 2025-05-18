from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os

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
class CodeRequest(BaseModel):
    code: str
    input: str = ""

@app.post("/run-python")
async def run_python_code(request: CodeRequest):
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
            temp_file.write(request.code)
            temp_file_path = temp_file.name

        # รัน python โค้ด พร้อมส่ง input
        result = subprocess.run(
            ["python", temp_file_path],
            input=request.input.encode(),
            capture_output=True,
            timeout=5,
            check=False,
        )

        os.remove(temp_file_path)  # ลบไฟล์ชั่วคราว

        output = result.stdout.decode() or result.stderr.decode()
        return {"output": output}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))