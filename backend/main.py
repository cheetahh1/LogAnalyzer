from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import analyzer # This is your pip-installed library
import uvicorn

app = FastAPI()

# Enable CORS so Vue can talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        log_text = content.decode("utf-8")
        
        # Runs your teammate's logic
        data = analyzer.parse_logs(log_text)
        
        return {"results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)