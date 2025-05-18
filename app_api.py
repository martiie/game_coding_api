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

class CodeRequest(BaseModel):
    source_code: str

@app.post("/run-python/")
def run_python_code(request: CodeRequest):
    code = request.source_code

    # สร้างไฟล์ชั่วคราว
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as tmp_file:
        tmp_file.write(code)
        filename = tmp_file.name

    try:
        # รัน python script ที่เขียนโดยให้ print ผลลัพธ์ main()
        # subprocess จะรันคำสั่ง python -c "from <filename> import main; print(main())"
        # แต่เราจะรันผ่านไฟล์โดยตรงพร้อมคำสั่ง print(main())
        command = [
            "python",
            "-c",
            f"import sys; sys.path.insert(0, '{os.path.dirname(filename)}'); "
            f"from {os.path.splitext(os.path.basename(filename))[0]} import main; "
            f"print(main())"
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr)

        output = result.stdout.strip()
        return {"output": output}

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=400, detail="Execution timed out")

    finally:
        os.remove(filename)
